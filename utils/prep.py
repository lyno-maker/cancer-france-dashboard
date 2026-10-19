"""Cleaning, column detection, validation and aggregated tables."""
import unicodedata
import pandas as pd

STD = ["dept_code", "dept", "period", "cancer", "sex", "rate", "cases"]
HINTS = {  # keywords searched in column names (order = priority); source columns are in French
    "dept_code": ["code_dep", "code_departement", "dep_code", "dept", "code"],
    "dept": ["libelle_dep", "nom_dep", "departement"],
    "period": ["periode", "annee", "year"],
    "cancer": ["site_label", "localisation", "cancer", "site"],
    "sex": ["sexe", "sex"],
    "rate": ["ratemonde", "taux_standard", "taux_std", "standardis", "rate", "taux"],
    "cases": ["nb_cas", "effectif"],
}


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return s.lower().strip().replace(" ", "_")


def detect_columns(df: pd.DataFrame) -> dict:
    """Guess which CSV column matches each standard field."""
    cols = {c: _norm(c) for c in df.columns}
    found, used = {}, set()
    for key in STD:
        for hint in HINTS[key]:
            match = [c for c, n in cols.items() if hint in n and c not in used]
            if match:
                found[key] = match[0]; used.add(match[0]); break
    return found


def clean(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    keys = [k for k, v in mapping.items() if v in df.columns]
    out = df[[mapping[k] for k in keys]].copy()
    out.columns = keys
    if "dept_code" in out:
        out["dept_code"] = out["dept_code"].astype(str).str.strip().str.upper().str.zfill(2)
    for c in ("rate", "cases"):
        if c in out:
            out[c] = pd.to_numeric(out[c].astype(str).str.replace(",", ".", regex=False), errors="coerce")
    if "period" in out:
        out["period"] = out["period"].astype(str).str.strip()
    return out.drop_duplicates().reset_index(drop=True)


def quality_report(raw: pd.DataFrame, df: pd.DataFrame) -> dict:
    miss = (df.isna().mean() * 100).round(1).rename("% missing").to_frame()
    return {
        "rows_raw": len(raw), "rows_clean": len(df),
        "duplicates_removed": int(raw.duplicated().sum()),
        "missing": miss,
        "negative_rates": int((df["rate"] < 0).sum()) if "rate" in df else 0,
        "depts": df["dept_code"].nunique() if "dept_code" in df else 0,
    }


def dept_table(df: pd.DataFrame) -> pd.DataFrame:
    keys = [c for c in ("dept_code", "dept") if c in df]
    return df.groupby(keys, as_index=False)["rate"].mean().dropna()


def trend_table(df: pd.DataFrame) -> pd.DataFrame:
    keys = ["period"] + (["sex"] if "sex" in df else [])
    return df.groupby(keys, as_index=False)["rate"].mean().sort_values("period")
