"""Chart functions: consistent style, labelled axes and units."""
import plotly.express as px
import streamlit as st

UNIT = "World age-standardised rate (per 100,000 person-years)"
SCALE = "YlOrRd"  # sequential, readable, good contrast
SEX_EN = {"Hommes": "Men", "Femmes": "Women", "Homme": "Men", "Femme": "Women"}


def _style(fig, title=None):
    fig.update_layout(title=title, margin=dict(l=10, r=10, t=50, b=10), template="plotly_white",
                      font=dict(size=14), legend_title_text="")
    return fig


def map_chart(tab, geojson):
    fig = px.choropleth_map(
        tab, geojson=geojson, locations="dept_code", featureidkey="properties.code",
        color="rate", color_continuous_scale=SCALE, hover_name="dept" if "dept" in tab else None,
        labels={"rate": UNIT, "dept_code": "Département code"}, map_style="carto-positron",
        zoom=4.3, center={"lat": 46.6, "lon": 2.4}, opacity=0.85)
    st.plotly_chart(_style(fig), use_container_width=True)


def bar_chart(tab, n=10, top=True):
    t = tab.nlargest(n, "rate") if top else tab.nsmallest(n, "rate")
    label = "dept" if "dept" in t else "dept_code"
    fig = px.bar(t.sort_values("rate"), x="rate", y=label, orientation="h", color="rate",
                 color_continuous_scale=SCALE, labels={"rate": UNIT, label: "Département"})
    fig.update_coloraxes(showscale=False)
    st.plotly_chart(_style(fig), use_container_width=True)


def line_chart(tab):
    tab = tab.copy()
    if "sex" in tab:
        tab["sex"] = tab["sex"].replace(SEX_EN)
    fig = px.line(tab, x="period", y="rate", color="sex" if "sex" in tab else None, markers=True,
                  labels={"period": "Period", "rate": UNIT, "sex": "Sex"})
    st.plotly_chart(_style(fig), use_container_width=True)


def dist_chart(tab, mean):
    fig = px.histogram(tab, x="rate", nbins=25, labels={"rate": UNIT, "count": "Number of départements"})
    fig.add_vline(x=mean, line_dash="dash", annotation_text=f"Mean: {mean:.0f}")
    st.plotly_chart(_style(fig), use_container_width=True)
