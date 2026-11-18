#!/usr/bin/env python3
"""Pon la fecha de última modificación en un solo paso (ejecútalo antes de build_en.py).

    python3 scripts/stamp_date.py            # usa la fecha y hora actuales
    python3 scripts/stamp_date.py 2026-11-17 # o una fecha concreta (hora 12:00)

Actualiza: dateModified del ProfilePage en index.html (fecha + hora + zona horaria,
que es lo que exige Google para ProfilePage), <lastmod> de / y /en/ en
sitemap.xml y la línea "Última actualización" de llms.txt y llms-full.txt.
(La página legal conserva su propia fecha: solo cámbiala cuando cambie su texto.)
"""
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
now = datetime.now().astimezone().replace(microsecond=0)  # hora local con su zona (+01:00 / +02:00)
if len(sys.argv) > 1:
    d = sys.argv[1]
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
        sys.exit("Formato de fecha: AAAA-MM-DD")
    dt = now.replace(**dict(zip(("year", "month", "day"), map(int, d.split("-")))), hour=12, minute=0, second=0).isoformat()
else:
    d = now.date().isoformat()
    dt = now.isoformat()


def sub(path, pattern, repl, flags=0):
    p = ROOT / path
    t = p.read_text(encoding="utf-8")
    new, n = re.subn(pattern, repl, t, flags=flags)
    if n == 0:
        print(f"  aviso: sin coincidencias en {path}", file=sys.stderr)
    p.write_text(new, encoding="utf-8")
    print(f"  {path}: {n} cambio(s)")


# ProfilePage (solo ese bloque: el dateModified que sigue a "inLanguage" del perfil)
sub("index.html", r'("@type": "ProfilePage".*?"dateModified": ")[^"]+', rf"\g<1>{dt}", re.S)
# sitemap: solo / y /en/ (no la página legal)
sub("sitemap.xml",
    r'(<loc>https://albertoortiz\.is-a\.dev/(?:en/)?</loc>\s*<lastmod>)\d{4}-\d{2}-\d{2}',
    rf"\g<1>{d}")
sub("llms.txt", r"(Última actualización: )\d{4}-\d{2}-\d{2}", rf"\g<1>{d}")
sub("llms-full.txt", r"(Última actualización: )\d{4}-\d{2}-\d{2}", rf"\g<1>{d}")
print("Ahora ejecuta: python3 scripts/build_en.py && python3 scripts/verify_site.py")
