import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

# Add dashboard folder to Python path
sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from data_loader import load_drug


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Drug Analysis | SignalQUBE",
    page_icon="💊",
    layout="wide"
)


# --------------------------------------------------
# LOAD DEPLOYMENT DATA
# --------------------------------------------------

drug_df = load_drug()

if drug_df.empty:
    st.warning("No signal data available.")
    st.stop()


# --------------------------------------------------
# CLEAN DRUG NAMES
# --------------------------------------------------

drug_df = drug_df.dropna(
    subset=["drugname"]
).copy()

drug_df["drugname"] = (
    drug_df["drugname"]
    .astype(str)
    .str.strip()
    .str.upper()
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("💊 Drug Analysis")

st.subheader(
    "Top Drugs Associated with Potential Safety Signals"
)


# --------------------------------------------------
# DATASET STATISTICS
# --------------------------------------------------

col1, col2, col3 = st.columns(3)


col1.metric(
    "💊 Signal Records",
    f"{len(drug_df):,}"
)


col2.metric(
    "🧬 Unique Drugs",
    f"{drug_df['drugname'].nunique():,}"
)


if "Signal" in drug_df.columns:

    strong_signals = len(
        drug_df[
            drug_df["Signal"]
            .astype(str)
            .str.contains(
                "Strong",
                case=False,
                na=False
            )
        ]
    )

else:
    strong_signals = 0


col3.metric(
    "🔴 Strong Signals",
    f"{strong_signals:,}"
)


st.markdown("---")


# --------------------------------------------------
# SEARCH DRUG
# --------------------------------------------------

search_drug = st.text_input(
    "🔍 Search Drug",
    placeholder="Type a drug name (e.g., ASPIRIN)"
)


filtered_df = drug_df.copy()


if search_drug:

    filtered_df = filtered_df[
        filtered_df["drugname"].str.contains(
            search_drug.strip().upper(),
            na=False,
            regex=False
        )
    ]


# --------------------------------------------------
# TOP N
# --------------------------------------------------

top_n = st.slider(
    "Select Top N Drugs",
    min_value=5,
    max_value=50,
    value=20
)


# --------------------------------------------------
# DRUG SUMMARY
# --------------------------------------------------

# Count signal records associated with each drug.
top_drugs = (
    filtered_df["drugname"]
    .value_counts()
    .head(top_n)
    .reset_index()
)


top_drugs.columns = [
    "Drug",
    "Signal Records"
]


# --------------------------------------------------
# CHART
# --------------------------------------------------

fig = px.bar(
    top_drugs,
    x="Signal Records",
    y="Drug",
    orientation="h",
    text="Signal Records",
    color="Signal Records",
    color_continuous_scale="Blues",
    title=f"Top {top_n} Drugs by Signal Records"
)


fig.update_traces(
    textposition="outside",
    hovertemplate=(
        "<b>%{y}</b>"
        "<br>Signal Records: %{x:,}"
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
    yaxis_title="Drug Name"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# --------------------------------------------------
# DRUG FREQUENCY TABLE
# --------------------------------------------------

st.markdown("---")

st.subheader("📋 Drug Signal Frequency Table")


display_df = top_drugs.copy()


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

        "Drug": st.column_config.TextColumn(
            "Drug",
            width="medium"
        ),

        "Signal Records": st.column_config.NumberColumn(
            "Signal Records",
            width=140,
            format="%d"
        )
    }
)


# --------------------------------------------------
# DOWNLOAD
# --------------------------------------------------

csv = top_drugs.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="📥 Download Drug Analysis CSV",
    data=csv,
    file_name="signalqube_top_drugs.csv",
    mime="text/csv"
)