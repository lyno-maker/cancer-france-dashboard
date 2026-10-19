import streamlit as st

def render():
    st.title("🧬 Cancer in France: where is the risk highest?")
    st.markdown("### 🎯 Hook\nAt the same age, the risk of cancer is **not the same from one département to another**. "
                "It is a territorial health inequality.")
    st.markdown("**Audience:** public-health decision makers (regional health agencies), students and the general public.  \n"
                "**Questions:** 1) Which territories are the most affected? 2) How large is the gap? "
                "3) How does the risk evolve over time, for women and men?")
    st.info("**Context:** rates are age-standardised (per 100,000 person-years), so départements with different "
            "age structures can be compared. Data come from cancer registries "
            "(partial territorial coverage, see *Limitations*).")
