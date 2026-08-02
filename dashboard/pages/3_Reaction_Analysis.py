import streamlit as st
import plotly.express as px
import sys

from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parent.parent))

from data_loader import load_reaction

st.set_page_config(
    page_title="Reaction Analysis",
    page_icon="⚠️",
    layout="wide"
)

reaction_df = load_reaction()

reaction_df = reaction_df.dropna(subset=["pt"])

reaction_df["pt"] = (
    reaction_df["pt"]
    .astype(str)
    .str.strip()
    .str.upper()
)

st.title("⚠️ Reaction Analysis")
st.subheader("Most Reported Adverse Reactions in FAERS")

col1, col2, col3 = st.columns(3)

col1.metric(
    "⚠️ Total Reaction Records",
    f"{len(reaction_df):,}"
)

col2.metric(
    "🧬 Unique Reactions",
    f"{reaction_df['pt'].nunique():,}"
)

col3.metric(
    "📄 Cases",
    f"{reaction_df['primaryid'].nunique():,}"
)

st.markdown("---")

search_reaction = st.text_input(
    "🔍 Search Reaction",
    placeholder="Type a reaction (e.g., HEADACHE)"
)

filtered_df = reaction_df.copy()

if search_reaction:
    filtered_df = filtered_df[
        filtered_df["pt"].str.contains(
            search_reaction.upper(),
            na=False
        )
    ]

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

top_reactions.columns = ["Reaction", "Reports"]

fig = px.bar(
    top_reactions,
    x="Reports",
    y="Reaction",
    orientation="h",
    text="Reports",
    color="Reports",
    color_continuous_scale="Reds",
    title=f"Top {top_n} Reported Reactions"
)

fig.update_traces(
    textposition="outside",
    hovertemplate="<b>%{y}</b><br>Reports: %{x:,}<extra></extra>"
)

fig.update_layout(
    template="plotly_dark",
    height=700,
    title_x=0.5,
    title_font_size=22,
    margin=dict(l=20, r=20, t=60, b=20),
    coloraxis_showscale=False,
    yaxis=dict(categoryorder="total ascending"),
    xaxis_title="Number of Reports",
    yaxis_title="Reaction"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

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
    height=400,
    column_config={
        "Sr. No.": st.column_config.NumberColumn(
            "Sr. No.",
            width=60
        ),
        "Reaction": st.column_config.TextColumn(
            "Reaction",
            width="medium"
        ),
        "Reports": st.column_config.NumberColumn(
            "Reports",
            width=120,
            format="%d"
        )
    }
)

csv = top_reactions.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Reaction Analysis CSV",
    data=csv,
    file_name="signalqube_top_reactions.csv",
    mime="text/csv"
)