import streamlit as st
from utils.io import load_data, load_geojson, SOURCE, LICENSE
from utils.prep import STD, detect_columns, clean, quality_report, dept_table, trend_table
from sections import intro, overview, deep_dives, conclusions

st.set_page_config(page_title="Cancer in France — Data Storytelling", page_icon="🧬", layout="wide")

# Labels shown in the UI for values that are in French in the source data
LABELS = {"Tous cancers": "All cancers", "Hommes": "Men", "Femmes": "Women", "Homme": "Men", "Femme": "Women"}
tr = lambda v: LABELS.get(v, v)


@st.cache_data(show_spinner="Loading data…")
def get_raw(uploaded):
    return load_data(uploaded)


@st.cache_data(show_spinner=False)
def get_geo():
    return load_geojson()


with st.sidebar:
    st.header("Filters")
    up = st.file_uploader("Local CSV (optional)", type="csv", help="Otherwise the data is downloaded automatically")
raw = get_raw(up.getvalue() if up else None)
mapping = detect_columns(raw)

with st.sidebar.expander("Detected columns (fix if needed)"):
    for k in STD:
        opts = ["—"] + list(raw.columns)
        sel = st.selectbox(k, opts, index=opts.index(mapping[k]) if k in mapping else 0, key=f"map_{k}")
        mapping.pop(k, None)
        if sel != "—":
            mapping[k] = sel

if not {"dept_code", "rate"} <= mapping.keys():
    st.error(f"Required columns not found (department code, rate). File columns: {list(raw.columns)}")
    st.stop()

df = clean(raw, mapping)
if "dept" not in df:
    names = {f["properties"]["code"]: f["properties"]["nom"] for f in get_geo()["features"]}
    names.update({"971": "Guadeloupe", "972": "Martinique", "973": "French Guiana", "974": "Réunion"})
    df["dept"] = df["dept_code"].map(names).fillna(df["dept_code"])
quality = quality_report(raw, df)

with st.sidebar:
    if "cancer" in df:
        cancers = sorted(df["cancer"].dropna().unique())
        cancer = st.selectbox("Cancer site", cancers, format_func=tr,
                              index=cancers.index("Tous cancers") if "Tous cancers" in cancers else 0)
        df = df[df["cancer"] == cancer]
    trend_base = df
    if "sex" in df:
        sexes = sorted(df["sex"].dropna().unique())
        sex = st.selectbox("Sex", sexes, format_func=tr)
        df = df[df["sex"] == sex]
    if "period" in df:
        periods = sorted(df["period"].unique())
        if len(periods) > 1:
            p0, p1 = st.select_slider("Periods", options=periods, value=(periods[0], periods[-1]))
            df = df[df["period"].between(p0, p1)]
            trend_base = trend_base[trend_base["period"].between(p0, p1)]

st.caption(f"Source: {SOURCE} — {LICENSE}")
dept_tab, trend_df = dept_table(df), trend_table(trend_base)
intro.render()
overview.render(df, trend_df, dept_tab, get_geo())
deep_dives.render(df, trend_df, dept_tab)
conclusions.render(dept_tab, trend_df, quality)
