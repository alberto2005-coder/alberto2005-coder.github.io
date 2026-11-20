#!/usr/bin/env python3
"""
Genera las versiones en inglés a partir de las páginas en español:
  index.html -> en/index.html
  informacion-legal/index.html -> en/informacion-legal/index.html

La web mantiene una única fuente de verdad: index.html (español) con los textos
en inglés en los atributos data-lang-en. Este script produce una página estática
con una URL propia por idioma (necesario para que Google indexe el inglés).

Uso (desde la raíz del repositorio):
    pip install beautifulsoup4
    python3 scripts/build_en.py

Ejecútalo cada vez que edites index.html y sube también en/index.html.
"""
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "index.html"
DST = ROOT / "en" / "index.html"
LEGAL_SRC = ROOT / "informacion-legal" / "index.html"
LEGAL_DST = ROOT / "en" / "informacion-legal" / "index.html"

BASE = "https://albertoortiz.is-a.dev"

TITLE_EN = "Alberto Ortiz Sánchez | Full Stack Developer in Granada"
DESC_EN = (
    "Full Stack Developer in Granada: custom websites, Odoo, PrestaShop, "
    "WordPress, Unity games and AI. Explore projects, experience and CV."
)

# Atributos accesibles que no llevan data-lang-*
ARIA_EN = {
    "Consentimiento de cookies": "Cookie consent",
    "Alberto O.S. — inicio": "Alberto O.S. — home",
    "Abrir menú": "Open menu",
    "Cambiar a tema oscuro": "Switch to dark theme",
    "Abrir menú de idioma": "Open language menu",
}
ALT_EN = {
    "Alberto Ortiz Sánchez — Logotipo": "Alberto Ortiz Sánchez — Logo",
    "The Memory Game, videojuego de memoria": "The Memory Game, memory video game",
    "The Memory Game — Videojuego publicado en Google Play Store":
        "The Memory Game — Video game published on Google Play Store",
    "Neon Dash, videojuego arcade de ritmo y velocidad":
        "Neon Dash, rhythm and speed arcade video game",
    "Neon Dash — Videojuego arcade de ritmo y velocidad en Itch.io":
        "Neon Dash — Rhythm and speed arcade video game on Itch.io",
    "Tetris C++, videojuego clásico desarrollado en C++":
        "Tetris C++, classic video game developed in C++",
    "Tetris C++ — Recreación clásica desarrollada en C++ en Itch.io":
        "Tetris C++ — Classic recreation developed in C++ on Itch.io",
    "Código QR con el enlace al portfolio de Alberto Ortiz Sánchez":
        "QR code linking to Alberto Ortiz Sánchez's portfolio",
}

# Datos estructurados (JSON-LD) que están en español en la página original
JSONLD_EN = {
    "jobTitle": "Full Stack Developer · Higher Technician in Multiplatform Application Development (DAM)",
    "description": (
        "Full Stack Developer in Granada specialised in web development, Odoo, "
        "PrestaShop, WordPress, Unity games and artificial intelligence."
    ),
}
KNOWS_ABOUT_EN = {
    "Desarrollo Full Stack": "Full Stack Development",
    "Inteligencia Artificial": "Artificial Intelligence",
    "Aprendizaje Automático": "Machine Learning",
    "Desarrollo de Videojuegos": "Game Development",
    "Ciberseguridad & OSINT": "Cybersecurity & OSINT",
    "Hacking Ético": "Ethical Hacking",
    "Criptografía y Cifrado AES-256": "Cryptography and AES-256 Encryption",
    "Creación de Compiladores e Intérpretes": "Compiler and Interpreter Design",
    "Odoo & PrestaShop ERP": "Odoo & PrestaShop ERP",
    "Docker y Despliegue de Aplicaciones": "Docker and Application Deployment",
}
ALUMNI_EN = {
    "Máster de FP en Aprendizaje Automático: Gestión de Datos y Entrenamiento":
        "Vocational Master's in Machine Learning: Data Management and Training",
    "Técnico Superior en Desarrollo de Aplicaciones Multiplataforma (DAM) y Bachillerato de Ciencias":
        "Higher Technician in Multiplatform Application Development (DAM) and Science Baccalaureate",
}
CRED_EN = {
    "Técnico Superior en Desarrollo de Aplicaciones Multiplataforma":
        "Higher Technician in Multiplatform Application Development",
    "Hacker Ético": "Ethical Hacker",
}


def set_meta(soup, attr, key, value):
    tag = soup.find("meta", attrs={attr: key})
    if tag is None:
        print(f"  aviso: no existe <meta {attr}={key!r}>", file=sys.stderr)
        return
    tag["content"] = value


def build_home():
    soup = BeautifulSoup(SRC.read_text(encoding="utf-8"), "html.parser")

    # --- Documento -----------------------------------------------------------
    soup.html["lang"] = "en"
    soup.title.string = TITLE_EN

    set_meta(soup, "name", "description", DESC_EN)
    set_meta(soup, "property", "og:title", TITLE_EN)
    set_meta(soup, "property", "og:description", DESC_EN)
    set_meta(soup, "property", "og:url", f"{BASE}/en/")
    set_meta(soup, "property", "og:locale", "en_US")
    set_meta(soup, "property", "og:locale:alternate", "es_ES")
    set_meta(soup, "property", "og:image", OG_IMAGE_EN)
    set_meta(soup, "name", "twitter:image", OG_IMAGE_EN)
    set_meta(soup, "property", "og:image:alt", "Alberto Ortiz Sánchez | Full Stack Developer")
    set_meta(soup, "name", "twitter:title", TITLE_EN)
    set_meta(soup, "name", "twitter:description", DESC_EN)
    set_meta(soup, "name", "twitter:image:alt", "Alberto Ortiz Sánchez | Full Stack Developer")
    canonical = soup.find("link", rel="canonical")
    canonical["href"] = f"{BASE}/en/"

    # El formulario de contacto vuelve a la portada del idioma activo aunque falle el JS
    redirect = soup.find("input", attrs={"name": "redirect"})
    if redirect is not None:
        redirect["value"] = f"{BASE}/en/"

    # --- Textos: equivalente estático de translatePage('en') -------------------
    for el in soup.select("[data-lang-en]"):
        html_en = el["data-lang-en"]
        el.clear()
        el.append(BeautifulSoup(html_en, "html.parser"))

    for el in soup.select("[data-placeholder-en]"):
        el["placeholder"] = el["data-placeholder-en"]

    for el in soup.find_all(attrs={"aria-label": True}):
        if el["aria-label"] in ARIA_EN:
            el["aria-label"] = ARIA_EN[el["aria-label"]]
    for el in soup.find_all("img", alt=True):
        if el["alt"] in ALT_EN:
            el["alt"] = ALT_EN[el["alt"]]
        elif el["alt"] and "data-lang-es" not in el.attrs:
            print(f"  aviso: alt sin traducir: {el['alt']!r}", file=sys.stderr)

    # Selector de idioma y CV en el idioma de la página
    soup.find(id="lang-label").string = "EN"
    for link in soup.select("[data-cv-link]"):
        link["href"] = link["data-cv-en"]
        link["hreflang"] = "en"
        link["aria-label"] = "Download CV as PDF"

    # --- Rutas relativas -> absolutas (la página vive en /en/) ----------------
    for el in soup.find_all(True):
        for attr in ("href", "src", "data-cv-es", "data-cv-en"):
            v = el.get(attr)
            if v and re.match(r"^assets/", v):
                el[attr] = "/" + v

    # --- Enlaces a la información legal: versión inglesa ---------------------
    for a in soup.find_all("a", href=re.compile(r"^/informacion-legal/")):
        a["href"] = "/en" + a["href"]

    # --- Datos estructurados ----------------------------------------------------
    for tag in soup.find_all("script", type="application/ld+json"):
        data = json.loads(tag.string)
        if data.get("@type") == "Person":
            data.update(JSONLD_EN)
            data["knowsAbout"] = [KNOWS_ABOUT_EN.get(k, k) for k in data.get("knowsAbout", [])]
            for a in data.get("alumniOf", []):
                a["description"] = ALUMNI_EN.get(a.get("description"), a.get("description"))
            for c in data.get("hasCredential", []):
                c["name"] = CRED_EN.get(c.get("name"), c.get("name"))
            data["mainEntityOfPage"] = {"@id": f"{BASE}/en/#profilepage"}
        if data.get("@type") == "ProfilePage":
            if isinstance(data.get("primaryImageOfPage"), dict):
                data["primaryImageOfPage"]["url"] = OG_IMAGE_EN
            data["@id"] = f"{BASE}/en/#profilepage"
            data["url"] = f"{BASE}/en/"
            data["name"] = TITLE_EN
            data["inLanguage"] = "en"
        if data.get("@type") == "ItemList":
            data["name"] = "Software projects by Alberto Ortiz Sánchez"
        tag.string = "\n" + json.dumps(data, ensure_ascii=False, indent=2) + "\n    "

    out = str(soup)
    out = out.replace(
        "<!DOCTYPE html>",
        "<!DOCTYPE html>\n<!-- ARCHIVO GENERADO por scripts/build_en.py a partir de index.html. "
        "No lo edites a mano: modifica index.html y vuelve a ejecutar el script. -->",
        1,
    )

    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(out, encoding="utf-8")
    print(f"OK  {DST.relative_to(ROOT)}  ({len(out):,} bytes)")


OG_IMAGE_EN = f"{BASE}/assets/img/og-image-en.png"
LEGAL_TITLE_EN = "Alberto Ortiz Sánchez | Legal information"
LEGAL_DESC_EN = (
    "Legal notice, privacy policy and cookie policy of the portfolio of "
    "Alberto Ortiz Sánchez."
)


def build_legal():
    soup = BeautifulSoup(LEGAL_SRC.read_text(encoding="utf-8"), "html.parser")
    url_en = f"{BASE}/en/informacion-legal/"

    soup.html["lang"] = "en"
    soup.title.string = LEGAL_TITLE_EN
    set_meta(soup, "name", "description", LEGAL_DESC_EN)
    set_meta(soup, "property", "og:title", LEGAL_TITLE_EN)
    set_meta(soup, "property", "og:description", LEGAL_DESC_EN)
    set_meta(soup, "property", "og:url", url_en)
    set_meta(soup, "property", "og:locale", "en_US")
    set_meta(soup, "property", "og:locale:alternate", "es_ES")
    set_meta(soup, "property", "og:image", OG_IMAGE_EN)
    set_meta(soup, "name", "twitter:image", OG_IMAGE_EN)
    set_meta(soup, "property", "og:image:alt", LEGAL_TITLE_EN)
    set_meta(soup, "name", "twitter:title", LEGAL_TITLE_EN)
    set_meta(soup, "name", "twitter:description", LEGAL_DESC_EN)
    set_meta(soup, "name", "twitter:image:alt", LEGAL_TITLE_EN)
    soup.find("link", rel="canonical")["href"] = url_en

    for el in soup.select("[data-lang-en]"):
        html_en = el["data-lang-en"]
        el.clear()
        el.append(BeautifulSoup(html_en, "html.parser"))
    for el in soup.find_all(attrs={"aria-label": True}):
        if el["aria-label"] in ARIA_EN:
            el["aria-label"] = ARIA_EN[el["aria-label"]]
    for el in soup.find_all("img", alt=True):
        if el["alt"] in ALT_EN:
            el["alt"] = ALT_EN[el["alt"]]
        elif el["alt"]:
            print(f"  aviso: alt sin traducir: {el['alt']!r}", file=sys.stderr)

    soup.find(id="lang-label").string = "EN"
    for link in soup.select("[data-cv-link]"):
        link["href"] = link["data-cv-en"]
        link["hreflang"] = "en"
        link["aria-label"] = "Download CV as PDF"
    # Enlaces a la propia legal (p. ej. banner de cookies): versión inglesa. El selector de idioma no se toca.
    for a in soup.find_all("a", href=re.compile(r"^/informacion-legal/")):
        if not a.get("data-lang"):
            a["href"] = "/en" + a["href"]
    # Enlaces a la portada: /en/ (el JS ya no los reescribe en páginas estáticas)
    for a in soup.select("[data-home]"):
        a["href"] = "/en/" + (a.get("data-home") or "")

    # Datos estructurados
    for tag in soup.find_all("script", type="application/ld+json"):
        data = json.loads(tag.string)
        if data.get("@type") == "WebPage":
            data["@id"] = f"{url_en}#webpage"
            data["url"] = url_en
            data["name"] = "Legal information | Alberto Ortiz Sánchez"
            data["description"] = LEGAL_DESC_EN
            data["inLanguage"] = "en"
            data["breadcrumb"] = {"@id": f"{url_en}#breadcrumb"}
        if data.get("@type") == "BreadcrumbList":
            data["@id"] = f"{url_en}#breadcrumb"
            data["itemListElement"][0].update({"name": "Home", "item": f"{BASE}/en/"})
            data["itemListElement"][1].update({"name": "Legal information", "item": url_en})
        tag.string = "\n" + json.dumps(data, ensure_ascii=False, indent=2) + "\n    "

    out = str(soup)
    out = out.replace(
        "<!DOCTYPE html>",
        "<!DOCTYPE html>\n<!-- ARCHIVO GENERADO por scripts/build_en.py a partir de informacion-legal/index.html. "
        "No lo edites a mano: modifica el original y vuelve a ejecutar el script. -->",
        1,
    )
    LEGAL_DST.parent.mkdir(parents=True, exist_ok=True)
    LEGAL_DST.write_text(out, encoding="utf-8")
    print(f"OK  {LEGAL_DST.relative_to(ROOT)}  ({len(out):,} bytes)")


# --------------------------------------------------------------------------------------
# Content-Security-Policy (meta). Una sola fuente de verdad para las 5 páginas.
# Sin 'unsafe-inline' en script-src: cada <script> en línea se autoriza por su hash SHA-256,
# que este script recalcula en cada ejecución. style-src conserva 'unsafe-inline' porque el
# CSS principal va incrustado y el widget de hCaptcha lo necesita.
# --------------------------------------------------------------------------------------
CSP_PAGES = ["index.html", "informacion-legal/index.html", "404.html",
             "en/index.html", "en/informacion-legal/index.html"]
CSP_TEMPLATE = (
    "default-src 'self'; "
    "img-src 'self' data: https: blob:; "
    "style-src 'self' 'unsafe-inline' https://newassets.hcaptcha.com; "
    "font-src 'self' https://newassets.hcaptcha.com; "
    "script-src 'self'{hashes} https://www.googletagmanager.com https://web3forms.com "
    "https://hcaptcha.com https://js.hcaptcha.com https://newassets.hcaptcha.com; "
    "connect-src 'self' https://api.github.com https://api.web3forms.com https://www.googletagmanager.com "
    "https://*.google-analytics.com https://*.analytics.google.com https://*.hcaptcha.com; "
    "media-src 'self'; manifest-src 'self'; object-src 'none'; base-uri 'self'; "
    "form-action 'self' https://api.web3forms.com; "
    "frame-src 'self' https://*.hcaptcha.com; "
    "upgrade-insecure-requests"
)
INLINE_SCRIPT_RE = re.compile(r"<script\b([^>]*)>(.*?)</script>", re.S)


def inline_script_hashes(html):
    import base64, hashlib
    out = []
    for attrs, body in INLINE_SCRIPT_RE.findall(html):
        if re.search(r"\bsrc\s*=", attrs) or "ld+json" in attrs:
            continue
        digest = hashlib.sha256(body.replace("\r\n", "\n").encode("utf-8")).digest()
        h = "'sha256-" + base64.b64encode(digest).decode() + "'"
        if h not in out:
            out.append(h)
    return out


def apply_csp(rel):
    p = ROOT / rel
    html = p.read_text(encoding="utf-8")
    hashes = inline_script_hashes(html)
    policy = CSP_TEMPLATE.format(hashes=(" " + " ".join(hashes)) if hashes else "")
    tag = f'<meta http-equiv="Content-Security-Policy"\n        content="{policy}">'
    new, n = re.subn(r'<meta\b[^>]*http-equiv="Content-Security-Policy"[^>]*>', lambda m: tag, html, count=1)
    if n != 1:
        print(f"  aviso: {rel} no tiene <meta> de CSP", file=sys.stderr)
        return
    if new != html:
        p.write_text(new, encoding="utf-8")
    print(f"CSP {rel}  ({len(hashes)} hash(es) de scripts en línea)")


def main():
    build_home()
    build_legal()
    for page in CSP_PAGES:
        apply_csp(page)


if __name__ == "__main__":
    main()
