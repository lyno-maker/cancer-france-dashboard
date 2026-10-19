"""Data loading (with disk cache) and map boundaries."""
import io, json
from pathlib import Path
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
# Dataset: Francim registries / INCa / Santé publique France (also listed on data.gouv.fr)
DATA_URL = ("https://odisse.santepubliquefrance.fr/api/explore/v2.1/catalog/datasets/"
            "cancer-incidence-observee-en-zone-registres-departement/exports/csv?delimiter=%3B&lang=fr")
GEO_URL = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson"
SOURCE = ("Observed incidence of invasive tumours in the départements covered by Francim cancer registries, "
          "1988-1992 to 2018-2022 — INCa / data.gouv.fr")
LICENSE = "License: Other (Public Domain)"
SEED = 42


def _fetch(url: str, path: Path) -> bytes:
    if not path.exists():
        DATA_DIR.mkdir(exist_ok=True)
        r = requests.get(url, timeout=90)
        r.raise_for_status()
        path.write_bytes(r.content)
    return path.read_bytes()


def load_data(uploaded: bytes | None = None) -> pd.DataFrame:
    content = uploaded if uploaded is not None else _fetch(DATA_URL, DATA_DIR / "raw.csv")
    return pd.read_csv(io.BytesIO(content), sep=None, engine="python", encoding="utf-8-sig")


def load_geojson() -> dict:
    return json.loads(_fetch(GEO_URL, DATA_DIR / "departements.geojson"))
