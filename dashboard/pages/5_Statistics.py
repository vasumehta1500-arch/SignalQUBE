import streamlit as st
import plotly.express as px
import pandas as pd
from data_loader import load_drug, load_reaction

st.set_page_config(
    page_title="Statistics",
    page_icon="📊",
    layout="wide"
)

drug = load_drug()
reaction = load_reaction()

drug = drug.dropna(subset=["drugname"])
drug["drugname"] = (
    drug["drugname"]
    .astype(str)
    .str.strip()
    .str.upper()
)

reaction = reaction.dropna(subset=["pt"])
reaction["pt"] = (
    reaction["pt"]
    .astype(str)
    .str.strip()
    .str.upper()
)

st.title("📊 SignalQUBE Statistics")
st.subheader("Overview of FAERS Pharmacovigilance Data")

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💊 Drug Records",
    f"{len(drug):,}"
)

col2.metric(
    "⚠️ Reaction Records",
    f"{len(reaction):,}"
)

col3.metric(
    "🧬 Unique Drugs",
    f"{drug['drugname'].nunique():,}"
)

col4.metric(
    "🩺 Unique Reactions",
    f"{reaction['pt'].nunique():,}"
)

st.markdown("---")

st.subheader("💊 Top 10 Most Reported Drugs")

top_drugs = (
    drug["drugname"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_drugs.columns = ["Drug", "Reports"]

fig1 = px.bar(
    top_drugs,
    x="Reports",
    y="Drug",
    orientation="h",
    text="Reports",
    color="Reports",
    color_continuous_scale="Blues"
)

fig1.update_layout(
    template="plotly_dark",
    height=500,
    title="Top 10 Reported Drugs",
    coloraxis_showscale=False,
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.markdown("---")

st.subheader("⚠️ Top 10 Most Reported Reactions")

top_reactions = (
    reaction["pt"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_reactions.columns = ["Reaction", "Reports"]

fig2 = px.bar(
    top_reactions,
    x="Reports",
    y="Reaction",
    orientation="h",
    text="Reports",
    color="Reports",
    color_continuous_scale="Reds"
)

fig2.update_layout(
    template="plotly_dark",
    height=500,
    title="Top 10 Reported Reactions",
    coloraxis_showscale=False,
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown("---")

st.subheader("📈 Suspect Drug Role Distribution")

suspect = drug[
    drug["role_cod"].isin(["PS", "SS"])
]

role_counts = (
    suspect["role_cod"]
    .value_counts()
    .reset_index()
)

role_counts.columns = ["Role", "Count"]

fig3 = px.pie(
    role_counts,
    names="Role",
    values="Count",
    hole=0.45,
    title="Primary vs Secondary Suspect Drugs"
)

fig3.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig3,
    use_container_width=True
)