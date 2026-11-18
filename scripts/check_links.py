#!/usr/bin/env python3
"""Comprueba todos los enlaces de las 4 páginas (y el sitemap) en la web publicada.

Solo usa la librería estándar: no hay que instalar nada.

    uv run python scripts/check_links.py                       # web real
    uv run python scripts/check_links.py --base http://localhost:8000   # servidor local
    uv run python scripts/check_links.py --solo-internos       # sin enlaces externos

Resultado: OK / REVISAR (bloqueos anti-bot: LinkedIn, Credly...) / ROTO.
Sale con código 1 si hay enlaces ROTOS.
"""
import argparse
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, urldefrag

ap = argparse.ArgumentParser()
ap.add_argument("--base", default="https://albertoortiz.is-a.dev")
ap.add_argument("--solo-internos", action="store_true")
args = ap.parse_args()
BASE = args.base.rstrip("/")
SITE_HOST = urlparse("https://albertoortiz.is-a.dev").netloc
PAGES = ["/", "/en/", "/informacion-legal/", "/en/informacion-legal/"]
UA = "Mozilla/5.0 (compatible; link-check/1.0; +https://albertoortiz.is-a.dev)"
BOT_WALLS = ("linkedin.com", "credly.com", "skillshop", "exceedlms.com", "play.google.com", "gamejolt.com", "itch.io")


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag in ("a", "link", "script", "img", "source", "iframe"):
            for k in ("href", "src"):
                if a.get(k):
                    self.links.append((tag, k, a[k]))


def fetch(url, method="GET", timeout=20):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.geturl(), (r.read().decode("utf-8", "replace") if method == "GET" else "")
    except urllib.error.HTTPError as e:
        return e.code, url, ""
    except Exception as e:  # noqa: BLE001
        return f"ERR {type(e).__name__}: {e}", url, ""


def to_local(u):
    """Reescribe URLs de producción a --base para poder probar en local."""
    p = urlparse(u)
    return BASE + (p.path or "/") + (("?" + p.query) if p.query else "") if p.netloc == SITE_HOST else u


found = {}   # url -> set(páginas)
anchors = {}  # página -> ids
problems = []
for path in PAGES:
    url = BASE + path
    st, final, html = fetch(url)
    if st != 200:
        problems.append(("ROTO", url, f"la página devuelve {st}"))
        continue
    c = Collector()
    c.feed(html)
    anchors[path] = c.ids
    for tag, attr, v in c.links:
        if v.startswith(("mailto:", "tel:", "data:", "javascript:")) or v == "#":
            continue
        full = to_local(urljoin(url, v))
        if v.startswith("#"):
            if v[1:] not in c.ids:
                problems.append(("ROTO", url, f"ancla {v} no existe en la página"))
            continue
        found.setdefault(full, set()).add(path)

# sitemap
st, _, xml = fetch(BASE + "/sitemap.xml")
if st == 200:
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    for loc in ET.fromstring(xml).findall("s:url/s:loc", ns):
        found.setdefault(to_local(loc.text.strip()), set()).add("sitemap.xml")
else:
    problems.append(("ROTO", BASE + "/sitemap.xml", f"devuelve {st}"))


def check(item):
    url, pages = item
    clean, frag = urldefrag(url)
    internal = urlparse(clean).netloc in (urlparse(BASE).netloc, SITE_HOST)
    if args.solo_internos and not internal:
        return None
    st, final, body = fetch(clean, "GET")
    if isinstance(st, int) and 200 <= st < 400:
        if internal and frag and body:
            c = Collector(); c.feed(body)
            if frag not in c.ids:
                return ("ROTO", url, pages, f"ancla #{frag} no existe en el destino")
        return ("OK", url, pages, st)
    if internal:
        return ("ROTO", url, pages, st)
    wall = any(w in url for w in BOT_WALLS)
    if wall and st in (401, 403, 405, 429, 999) or (wall and isinstance(st, str)):
        return ("REVISAR", url, pages, f"{st} (bloquea bots: ábrelo a mano)")
    return ("ROTO", url, pages, st)


with ThreadPoolExecutor(8) as ex:
    results = [r for r in ex.map(check, sorted(found.items())) if r]

ok = [r for r in results if r[0] == "OK"]
rev = [r for r in results if r[0] == "REVISAR"]
bad = [r for r in results if r[0] == "ROTO"]
for tag, url, pages, info in rev + bad:
    print(f"{tag:8} {url}\n         -> {info}   [en: {', '.join(sorted(pages))}]")
for tag, url, info in problems:
    print(f"{tag:8} {url}\n         -> {info}")
print(f"\n{len(ok)} OK · {len(rev)} para revisar a mano · {len(bad) + len(problems)} rotos")
sys.exit(1 if bad or problems else 0)
