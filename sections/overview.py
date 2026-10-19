import streamlit as st
from utils import viz

def render(df_f, trend_df, dept_tab, geojson):
    st.header("1. Overview")
    if dept_tab.empty:
        st.warning("No data for these filters."); return
    mean = dept_tab["rate"].mean()
    hi, lo = dept_tab.loc[dept_tab["rate"].idxmax()], dept_tab.loc[dept_tab["rate"].idxmin()]
    name = lambda r: r["dept"] if "dept" in r else r["dept_code"]
    delta = None
    tt = df_f.groupby("period")["rate"].mean()
    if len(tt) > 1:
        first, last = tt.index[0], tt.index[-1]
        a = df_f[df_f["period"] == first].groupby("dept_code")["rate"].mean()
        b = df_f[df_f["period"] == last].groupby("dept_code")["rate"].mean()
        common = a.index.intersection(b.index)
        if len(common):
            delta = f"{(b[common].mean() - a[common].mean()):+.1f} vs {first} (same départements)"
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Mean rate", f"{mean:.0f} /100,000", delta, help="Mean across départements, filters applied")
    c2.metric("Départements covered", len(dept_tab))
    c3.metric("Highest rate", f"{hi['rate']:.0f}", str(name(hi)), delta_color="off")
    c4.metric("Max / min ratio", f"×{hi['rate'] / lo['rate']:.2f}", help="Gap between the extreme départements")
    st.subheader("Map: an unequal risk across territories")
    viz.map_chart(dept_tab, geojson)
    st.caption("Choropleth map of départements: the darker the colour, the higher the age-standardised rate. "
               "Overseas départements are not shown on the map.")
