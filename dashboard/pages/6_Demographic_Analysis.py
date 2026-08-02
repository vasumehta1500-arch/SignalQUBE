import streamlit as st
import plotly.express as px
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from data_loader import load_demo

st.set_page_config(
    page_title="Demographic Analysis",
    page_icon="👥",
    layout="wide"
)

demo = load_demo()

st.title("👥 Demographic Analysis")
st.subheader("Patient Demographics from FAERS")

st.markdown("---")

col1, col2, col3 = st.columns(3)

col1.metric(
    "📄 Total Cases",
    f"{len(demo):,}"
)

male = len(demo[demo["sex"] == "M"])
female = len(demo[demo["sex"] == "F"])

col2.metric(
    "👨 Male Cases",
    f"{male:,}"
)

col3.metric(
    "👩 Female Cases",
    f"{female:,}"
)

st.markdown("---")

st.subheader("👥 Gender Distribution")

gender = (
    demo["sex"]
    .fillna("Unknown")
    .replace({
        "M": "Male",
        "F": "Female",
        "UNK": "Unknown"
    })
    .value_counts()
    .reset_index()
)

gender.columns = ["Gender", "Cases"]

fig = px.pie(
    gender,
    names="Gender",
    values="Cases",
    hole=0.45,
    title="Gender Distribution"
)

fig.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

st.subheader("🎂 Age Distribution")

ages = demo.copy()

ages["age"] = ages["age"].fillna(0)

ages = ages[
    (ages["age"] > 0) &
    (ages["age"] < 120)
]

fig2 = px.histogram(
    ages,
    x="age",
    nbins=30,
    title="Patient Age Distribution"
)

fig2.update_layout(
    template="plotly_dark",
    height=500,
    xaxis_title="Age",
    yaxis_title="Cases"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown("---")

st.subheader("🌍 Top Reporting Countries")

countries = (
    demo["reporter_country"]
    .fillna("Unknown")
    .value_counts()
    .head(10)
    .reset_index()
)

countries.columns = ["Country", "Reports"]

fig3 = px.bar(
    countries,
    x="Reports",
    y="Country",
    orientation="h",
    text="Reports",
    color="Reports",
    color_continuous_scale="Viridis"
)

fig3.update_layout(
    template="plotly_dark",
    height=500,
    coloraxis_showscale=False,
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(
    fig3,
    use_container_width=True
)