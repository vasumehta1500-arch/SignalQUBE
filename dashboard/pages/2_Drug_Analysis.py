import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path





sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils import load_drug

from data_loader import load_drug

drug_df = load_drug()

drug_df = drug_df.dropna(subset=["drugname"])

drug_df["drugname"] = (
    drug_df["drugname"]
    .astype(str)
    .str.strip()
    .str.upper()
)

st.title("💊 Drug Analysis")
st.subheader("Top Reported Drugs in FAERS")

col1, col2, col3 = st.columns(3)

col1.metric(
    "💊 Total Drug Records",
    f"{len(drug_df):,}"
)

col2.metric(
    "🧬 Unique Drugs",
    f"{drug_df['drugname'].nunique():,}"
)

col3.metric(
    "⚠️ Suspect Drug Records",
    f"{len(drug_df[drug_df['role_cod'].isin(['PS', 'SS'])]):,}"
)

st.markdown("---")

search_drug = st.text_input(
    "🔍 Search Drug",
    placeholder="Type a drug name (e.g., ASPIRIN)"
)

filtered_df = drug_df.copy()

if search_drug:
    filtered_df = filtered_df[
        filtered_df["drugname"].str.contains(
            search_drug.upper(),
            na=False
        )
    ]

top_n = st.slider(
    "Select Top N Drugs",
    min_value=5,
    max_value=50,
    value=20
)

top_drugs = (
    filtered_df["drugname"]
    .value_counts()
    .head(top_n)
    .reset_index()
)

top_drugs.columns = ["Drug", "Reports"]

fig = px.bar(
    top_drugs,
    x="Reports",
    y="Drug",
    orientation="h",
    text="Reports",
    color="Reports",
    color_continuous_scale="Blues",
    title=f"Top {top_n} Reported Drugs"
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
    yaxis_title="Drug Name"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.subheader("📋 Drug Frequency Table")

display_df = top_drugs.copy()
display_df.insert(0, "Sr. No.", range(1, len(display_df) + 1))

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
        "Drug": st.column_config.TextColumn(
            "Drug",
            width="medium"
        ),
        "Reports": st.column_config.NumberColumn(
            "Reports",
            width=120,
            format="%d"
        )
    }
)

csv = top_drugs.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Drug Analysis CSV",
    data=csv,
    file_name="signalqube_top_drugs.csv",
    mime="text/csv"
)