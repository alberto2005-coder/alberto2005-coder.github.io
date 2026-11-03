#!/usr/bin/env python3
"""
Genera la versión en inglés (/en/index.html) a partir de index.html.

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
    "jobTitle": "Full Stack Developer · Higher Technician in Multiplatform App Development (DAM)",
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
}


def set_meta(soup, attr, key, value):
    tag = soup.find("meta", attrs={attr: key})
    if tag is None:
        print(f"  aviso: no existe <meta {attr}={key!r}>", file=sys.stderr)
        return
    tag["content"] = value


def main():
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
    set_meta(soup, "property", "og:image:alt", "Alberto Ortiz Sánchez — Full Stack Developer")
    set_meta(soup, "name", "twitter:title", TITLE_EN)
    set_meta(soup, "name", "twitter:description", DESC_EN)
    canonical = soup.find("link", rel="canonical")
    canonical["href"] = f"{BASE}/en/"

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


if __name__ == "__main__":
    main()
