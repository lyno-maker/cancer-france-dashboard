import streamlit as st
from utils import viz

def render(df_f, trend_df, dept_tab):
    st.header("2. Deep dives")
    if dept_tab.empty:
        return
    st.subheader("Ranking: the extremes")
    n = st.slider("Number of départements shown", 5, 20, 10, help="Top / bottom N")
    a, b = st.columns(2)
    with a:
        st.markdown("**Highest rates**"); viz.bar_chart(dept_tab, n, True)
    with b:
        st.markdown("**Lowest rates**"); viz.bar_chart(dept_tab, n, False)
    st.caption("Horizontal bars: age-standardised rate per département, ranked from highest to lowest.")
    st.subheader("Evolution over time")
    viz.line_chart(trend_df)
    st.caption("Lines: mean rate per period, by sex. X axis: period, Y axis: rate per 100,000.")
    st.subheader("Distribution: inequality at a glance")
    viz.dist_chart(dept_tab, dept_tab["rate"].mean())
    st.caption("Histogram of the number of départements per rate level; the dashed line marks the mean.")
