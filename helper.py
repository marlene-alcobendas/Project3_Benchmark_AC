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

