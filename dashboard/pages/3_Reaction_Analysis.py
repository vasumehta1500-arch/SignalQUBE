import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from data_loader import load_reaction


st.set_page_config(
    page_title="Reaction Analysis",
    page_icon="⚠️",
    layout="wide"
)


# -----------------------------------
# Load deployment data
# -----------------------------------

reaction_df = load_reaction()


# -----------------------------------
# Clean reaction names
# -----------------------------------

reaction_df = reaction_df.dropna(
    subset=["pt"]
).copy()

reaction_df["pt"] = (
    reaction_df["pt"]
    .astype(str)
    .str.strip()
    .str.upper()
)


# -----------------------------------
# Header
# -----------------------------------

st.title("⚠️ Reaction Analysis")

st.subheader(
    "Most Reported Adverse Reactions in FAERS"
)


# -----------------------------------
# Statistics
# -----------------------------------

col1, col2 = st.columns(2)

col1.metric(
    "⚠️ Total Signal Records",
    f"{len(reaction_df):,}"
)

col2.metric(
    "🧬 Unique Reactions",
    f"{reaction_df['pt'].nunique():,}"
)

st.markdown("---")


# -----------------------------------
# Search
# -----------------------------------

search_reaction = st.text_input(
    "🔍 Search Reaction",
    placeholder="Type a reaction name"
)

filtered_df = reaction_df.copy()

if search_reaction:

    filtered_df = filtered_df[
        filtered_df["pt"].str.contains(
            search_reaction.upper(),
            na=False
        )
    ]


# -----------------------------------
# Top N
# -----------------------------------

top_n = st.slider(
    "Select Top N Reactions",
    min_value=5,
    max_value=50,
    value=20
)


top_reactions = (
    filtered_df["pt"]
    .value_counts()
    .head(top_n)
    .reset_index()
)

top_reactions.columns = [
    "Reaction",
    "Reports"
]


# -----------------------------------
# Chart
# -----------------------------------

fig = px.bar(
    top_reactions,
    x="Reports",
    y="Reaction",
    orientation="h",
    text="Reports",
    color="Reports",
    color_continuous_scale="Blues",
    title=f"Top {top_n} Reported Adverse Reactions"
)

fig.update_traces(
    textposition="outside",
    hovertemplate=(
        "<b>%{y}</b>"
        "<br>Records: %{x:,}"
        "<extra></extra>"
    )
)

fig.update_layout(
    template="plotly_dark",
    height=700,
    title_x=0.5,
    title_font_size=22,
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    ),
    coloraxis_showscale=False,
    yaxis=dict(
        categoryorder="total ascending"
    ),
    xaxis_title="Number of Signal Records",
    yaxis_title="Adverse Reaction"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# -----------------------------------
# Table
# -----------------------------------

st.markdown("---")

st.subheader("📋 Reaction Frequency Table")


display_df = top_reactions.copy()

display_df.insert(
    0,
    "Sr. No.",
    range(1, len(display_df) + 1)
)


st.dataframe(
    display_df,
    hide_index=True,
    use_container_width=True,
    height=400
)


# -----------------------------------
# Download
# -----------------------------------

csv = top_reactions.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="📥 Download Reaction Analysis CSV",
    data=csv,
    file_name="signalqube_top_reactions.csv",
    mime="text/csv"
)