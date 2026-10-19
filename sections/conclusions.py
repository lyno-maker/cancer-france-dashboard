import streamlit as st

def render(dept_tab, trend_df, quality):
    st.header("3. Data quality & limitations")
    c1, c2, c3 = st.columns(3)
    c1.metric("Raw rows", quality["rows_raw"]); c2.metric("Duplicates removed", quality["duplicates_removed"])
    c3.metric("Negative rates", quality["negative_rates"])
    st.dataframe(quality["missing"], use_container_width=True)
    st.info("**Limitations:** registries cover only part of the départements (21 here, including overseas "
            "départements that are absent from the map); association ≠ causation (gaps also reflect screening, "
            "behaviours and environment); the mean rate is a simple average of départements, not weighted by "
            "population. Data are aggregated: no re-identification risk.")
    st.header("4. Key insights & next steps")
    if not dept_tab.empty:
        hi = dept_tab.nlargest(1, "rate").iloc[0]; lo = dept_tab.nsmallest(1, "rate").iloc[0]
        lab = lambda r: r["dept"] if "dept" in r else r["dept_code"]
        st.success(f"**Insight:** with the current filters, the gap between {lab(hi)} ({hi['rate']:.0f}) and "
                   f"{lab(lo)} ({lo['rate']:.0f}) is a factor of ×{hi['rate'] / lo['rate']:.2f}.")
    st.markdown("**Implications:** target screening and prevention on the most affected territories.  \n"
                "**Next steps:** cross with socio-economic or environmental data (GD4H).")
