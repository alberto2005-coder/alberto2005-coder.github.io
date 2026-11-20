#!/usr/bin/env python3
"""
Comprobaciones estáticas del sitio (sin red). Úsalo antes de cada push:

    pip install beautifulsoup4
    python3 scripts/verify_site.py

Comprueba:
  1. en/index.html está al día respecto a index.html (si no, ejecuta build_en.py).
  2. Todos los enlaces/recursos internos apuntan a archivos que existen.
  3. Canonical y hreflang son coherentes (reciprocidad) y apuntan a URLs reales.
  4. Las URLs del sitemap.xml existen y coinciden con los canonical.
  5. Los bloques JSON-LD son JSON válido.
  6. El CSS incrustado en index.html contiene assets/css/style.css (404.html lo usa enlazado).
Devuelve código de salida 1 si hay errores.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://albertoortiz.is-a.dev"
PAGES = ["index.html", "en/index.html", "informacion-legal/index.html", "en/informacion-legal/index.html", "404.html"]
errors, warnings = [], []


def err(msg):
    errors.append(msg)


def url_to_file(path: str):
    """Ruta URL (sin dominio) -> archivo del repo (como lo sirve GitHub Pages)."""
    path = path.split("#")[0].split("?")[0]
    if path.endswith("/"):
        path += "index.html"
    f = ROOT / path.lstrip("/")
    if f.is_dir():
        f = f / "index.html"
    return f


def soup_of(rel):
    return BeautifulSoup((ROOT / rel).read_text(encoding="utf-8"), "html.parser")


# 1) en/index.html al día ------------------------------------------------------------
GENERATED = list(PAGES)  # build_en.py regenera EN y recalcula la CSP de todas
current = {g: (ROOT / g).read_text(encoding="utf-8") for g in GENERATED if (ROOT / g).exists()}
with tempfile.TemporaryDirectory() as tmp:
    # Se regenera en memoria ejecutando el script sobre una copia
    import shutil
    shutil.copytree(ROOT, Path(tmp) / "r", ignore=shutil.ignore_patterns(".git"))
    subprocess.run([sys.executable, str(Path(tmp) / "r" / "scripts" / "build_en.py")],
                   check=True, capture_output=True)
    for g in GENERATED:
        fresh = (Path(tmp) / "r" / g).read_text(encoding="utf-8")
        if current.get(g) != fresh:
            err(f"{g} está desactualizado (versión EN o hashes de la CSP): ejecuta  build_en.py")

# 2) enlaces y recursos internos -----------------------------------------------------
for rel in PAGES:
    page_url_dir = "/" + str(Path(rel).parent).replace(".", "").strip("/")
    page_url_dir = page_url_dir.rstrip("/") + "/"
    for el in soup_of(rel).find_all(True):
        for attr in ("href", "src"):
            v = el.get(attr)
            if not v or v.startswith(("#", "mailto:", "tel:", "data:", "javascript:")):
                continue
            u = urlparse(v)
            if u.scheme in ("http", "https"):
                if u.netloc != "albertoortiz.is-a.dev":
                    continue
                target = u.path or "/"
            elif v.startswith("/"):
                target = u.path
            else:
                target = page_url_dir + u.path  # relativo
            f = url_to_file(target)
            if not f.exists():
                err(f"{rel}: <{el.name} {attr}={v!r}> -> no existe {f.relative_to(ROOT)}")
            if target.endswith("index.html") and attr == "href" and el.name == "a":
                err(f"{rel}: enlace a {v!r}: usa la URL limpia (/ o /en/) para no duplicar contenido")

# 3) canonical y hreflang ---------------------------------------------------------------
canon = {}
for rel in PAGES:
    s = soup_of(rel)
    c = s.find("link", rel="canonical")
    if rel == "404.html":
        continue
    if not c:
        err(f"{rel}: falta canonical")
        continue
    canon[rel] = c["href"]
    f = url_to_file(urlparse(c["href"]).path)
    if not f.exists():
        err(f"{rel}: el canonical {c['href']} no corresponde a ningún archivo")
    og = s.find("meta", property="og:url")
    if og and og["content"] != c["href"]:
        err(f"{rel}: og:url ({og['content']}) distinto del canonical ({c['href']})")

# Pares de idiomas: (página ES, página EN)
for es_rel, en_rel in (("index.html", "en/index.html"),
                       ("informacion-legal/index.html", "en/informacion-legal/index.html")):
    alts = {}
    for rel in (es_rel, en_rel):
        alts[rel] = {l["hreflang"]: l["href"] for l in soup_of(rel).find_all("link", rel="alternate") if l.get("hreflang")}
    if alts[es_rel] != alts[en_rel]:
        err(f"hreflang distinto entre {es_rel} y {en_rel} (deben ser idénticos y recíprocos)")
    for lang, href in alts[es_rel].items():
        if not url_to_file(urlparse(href).path).exists():
            err(f"hreflang {lang}: {href} no existe")
    if alts[es_rel].get("es") != canon.get(es_rel) or alts[es_rel].get("en") != canon.get(en_rel):
        err(f"hreflang de {es_rel} no coincide con los canonical")
    if alts[es_rel].get("x-default") != canon.get(es_rel):
        err(f"x-default de {es_rel} debería apuntar a la versión en español")

# 4) sitemap ----------------------------------------------------------------------------
ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
try:
    locs = [u.text for u in ET.parse(ROOT / "sitemap.xml").getroot().findall("s:url/s:loc", ns)]
except ET.ParseError as e:
    err(f"sitemap.xml no es XML válido: {e}")
    locs = []
for loc in locs:
    if not url_to_file(urlparse(loc).path).exists():
        err(f"sitemap: {loc} no existe")
for rel, c in canon.items():
    if c not in locs:
        err(f"sitemap: falta {c}")
for loc in locs:
    if loc not in canon.values():
        err(f"sitemap: {loc} no es canonical de ninguna página")

# 5) JSON-LD ------------------------------------------------------------------------------
for rel in ("index.html", "en/index.html", "informacion-legal/index.html", "en/informacion-legal/index.html"):
    for i, t in enumerate(soup_of(rel).find_all("script", type="application/ld+json")):
        try:
            json.loads(t.string)
        except Exception as e:  # noqa: BLE001
            err(f"{rel}: JSON-LD #{i} inválido: {e}")

# 6) CSS incrustado == assets/css/style.css ---------------------------------------------------
norm = lambda x: re.sub(r"\s+", " ", x).strip()
css = norm((ROOT / "assets" / "css" / "style.css").read_text(encoding="utf-8"))
inline = norm(" ".join(t.get_text() for t in soup_of("index.html").find_all("style")))
if css not in inline:
    warnings.append("El CSS incrustado de index.html no coincide con assets/css/style.css "
                    "(sincronízalos: el comentario de index.html dice que son copia exacta).")

# 7) Seguridad: CSP sin 'unsafe-inline' en scripts, hashes al día, sin recursos de terceros no previstos ----------
ALLOWED_SCRIPT_HOSTS = {"https://www.googletagmanager.com", "https://web3forms.com", "https://hcaptcha.com",
                        "https://js.hcaptcha.com", "https://newassets.hcaptcha.com"}
for rel in PAGES:
    html = (ROOT / rel).read_text(encoding="utf-8")
    m = re.search(r'http-equiv="Content-Security-Policy"\s+content="([^"]*)"', html)
    if not m:
        err(f"{rel}: falta la Content-Security-Policy"); continue
    dirs = {d.split()[0]: d.split()[1:] for d in m.group(1).split(";") if d.strip()}
    sc = dirs.get("script-src", [])
    if "'unsafe-inline'" in sc or "'unsafe-eval'" in sc:
        err(f"{rel}: script-src no debe llevar 'unsafe-inline' ni 'unsafe-eval'")
    if "frame-ancestors" in dirs:
        warnings.append(f"{rel}: frame-ancestors no funciona en <meta> (se ignora)")
    for host in [s for s in sc if s.startswith("https://")]:
        if host not in ALLOWED_SCRIPT_HOSTS:
            err(f"{rel}: script-src permite un host no previsto: {host}")
    for attrs, body in re.findall(r"<script\b([^>]*)>(.*?)</script>", html, re.S):
        if re.search(r"\bsrc\s*=", attrs) or "ld+json" in attrs:
            continue
        import base64, hashlib
        h = "'sha256-" + base64.b64encode(hashlib.sha256(body.replace("\r\n", "\n").encode("utf-8")).digest()).decode() + "'"
        if h not in sc:
            err(f"{rel}: un <script> en línea no está autorizado en la CSP (ejecuta build_en.py)")
    if re.search(r"\s(on(click|load|error|mouseover|submit|change|focus|blur)|style)=\"", html) and rel != "404.html":
        bad = re.findall(r"\s(on\w+)=\"", html)
        if bad:
            err(f"{rel}: atributos de evento en línea ({', '.join(sorted(set(bad)))}): no caben en una CSP estricta")
    for el in soup_of(rel).find_all(["script", "link", "img", "iframe"]):
        u = el.get("src") or el.get("href") or ""
        if u.startswith("http") and not u.startswith(BASE) and el.name in ("script", "iframe") :
            err(f"{rel}: <{el.name}> carga un recurso externo en HTML: {u}")
        if any(x in u for x in ("fonts.googleapis.com", "fonts.gstatic.com", "cdnjs.cloudflare.com")):
            err(f"{rel}: recurso de CDN de terceros que ya está autoalojado: {u}")

# Resultado ---------------------------------------------------------------------------------
for w in warnings:
    print("AVISO ", w)
for e in errors:
    print("ERROR ", e)
print(f"\n{len(errors)} error(es), {len(warnings)} aviso(s)")
sys.exit(1 if errors else 0)
