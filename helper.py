

### WEB SCRAPER PARA AVIATION SAFETY NETWORK (ASN)

import time, random, re, json
from pathlib import Path
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup

BASE = "https://aviation-safety.net"
CAT  = "ACE"  # Engines
HEADERS = {"User-Agent": "Mozilla/5.0 (master-project; contact: you@example.com)"}
CACHE_DIR = Path("asn_cache"); CACHE_DIR.mkdir(exist_ok=True)

# --- utilidades ---
def get(url: str, sleep=(1.2, 2.5), retries=3) -> Optional[str]:
    for i in range(retries):
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            if r.status_code == 200:
                time.sleep(random.uniform(*sleep))
                return r.text
        except requests.RequestException:
            pass
        time.sleep(1.5 * (i + 1))
    return None

def cache_get(url: str) -> Optional[str]:
    key = re.sub(r"[^a-zA-Z0-9_-]+", "_", url.strip("/"))
    fp = CACHE_DIR / f"{key}.html"
    if fp.exists():
        return fp.read_text(encoding="utf-8", errors="ignore")
    html = get(url)
    if html:
        fp.write_text(html, encoding="utf-8")
    return html

# --- parseador de la página de categoría (solo lista) ---
def parse_cat_page(html: str) -> List[Dict]:
    """Extrae filas visibles (sin entrar al detalle) de una página /asndb/cat/ACE/{n}."""
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    # Tabla con columnas: fecha | aeronave | reg/operador | lugar (pueden variar)
    for tr in soup.select("table tr"):
        tds = tr.select("td")
        if len(tds) < 4:
            continue

        date_txt = tds[0].get_text(" ", strip=True)
        ac_txt   = tds[1].get_text(" ", strip=True)
        reg_op   = tds[2].get_text(" ", strip=True)
        place    = tds[3].get_text(" ", strip=True)

        # Heurística de matrícula (sin abrir detalle)
        reg = None
        reg_compact = re.sub(r"\s+", "", reg_op)
        m = re.search(r"\b([A-Z]{1,2}-?[A-Z0-9]{2,5})\b", reg_compact)
        if m:
            reg = m.group(1)

        rows.append({
            "date_text": date_txt,
            "aircraft_text": ac_txt,
            "reg_op_text": reg_op,
            "registration": reg,
            "location_text": place
        })
    return rows

# --- scraper principal (SIN entrar al detalle) ---
def scrape_category_ACE_list_only(max_pages=2000) -> List[Dict]:
    out = []
    page = 1
    while page <= max_pages:
        url = f"{BASE}/asndb/cat/{CAT}/{page}"
        html = cache_get(url)
        if not html:
            break

        rows = parse_cat_page(html)
        if not rows:
            # página sin resultados -> fin
            break

        out.extend(rows)
        page += 1
    return out




### NORMALIZACIÓN DE MATRÍCULAS AERONÁUTICAS


import pandas as pd

# 1) Normaliza matrícula (quitar espacios, mayúsculas, mantener guion)
def norm_reg(s: pd.Series) -> pd.Series:
    return (s.astype("string")
              .str.strip()
              .str.upper()
              .str.replace(" ", "", regex=False))

# 2) patrones clave
US_N = re.compile(r"^N\d{1,5}[A-Z]{0,2}$")            # N123, N12345, N123AB
HAS_DASH = re.compile(r"-")

def normalize_registration(reg: str) -> str | None:
    """Normaliza matrículas manteniendo los formatos correctos:
       - USA N-nnnnnLL  -> sin guion
       - Canadá C-F/Gxxx -> con guion (inserta si falta)
       - Prefijos de 1 letra (G,F,D,I,O,Y,M,S,T) -> G-ABCD, etc.
       - Prefijos de 2 chars (EC, PH, OO, 9V, 4X, etc.) -> EC-KGJ, 9V-ABC, etc.
    """
    if pd.isna(reg):
        return None
    s = re.sub(r"\s+", "", str(reg).upper())
    s = re.sub(r"-{2,}", "-", s)  # colapsa guiones múltiples

    # si ya lleva guion y no es una rareza, respeta
    if HAS_DASH.search(s):
        # caso Canadá ya correcto C-Fxxx / C-Gxxx
        if re.match(r"^C-[FG][A-Z]{3}$", s):
            return s
        return s

    # USA: N + 1-5 dígitos + 0-2 letras -> sin guion
    if US_N.match(s):
        return s

    # Canadá sin guion: C F/G + 3 letras -> inserta guion tras C
    if re.match(r"^C[FG][A-Z]{3}$", s):
        return f"C-{s[1:]}"

    # Prefijo de 1 letra + 4 letras (GABCD, FXXXX, DXXXX, IXXXX, etc.)
    if len(s) == 5 and s[0] in set("GFDIOYMSTC") and s[1:].isalpha():
        return f"{s[0]}-{s[1:]}"

    # Prefijo de 2 chars (incluye dígitos: 9V, 4X, 5Y...) + 3–5 alfanum
    m = re.match(r"^([A-Z0-9]{2})([A-Z0-9]{3,5})$", s)
    if m and not s.startswith("N"):  # ya cubrimos N arriba
        return f"{m.group(1)}-{m.group(2)}"

    # si no encaja en ninguna regla, devuelve limpio tal cual
    return s

def norm_reg_series(s: pd.Series) -> pd.Series:
    return s.astype("string").apply(normalize_registration)