import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.analysis.signal_detection import SignalDetector

st.set_page_config(
    page_title="Signal Ranking",
    page_icon="🏆",
    layout="wide"
)

@st.cache_resource
def get_detector():
    return SignalDetector()

detector = get_detector()

st.title("🏆 Signal Ranking")
st.subheader("Top Drug-Reaction Signals in SignalQUBE")

with st.spinner("Calculating signal rankings..."):
    pairs = detector.top_drug_reaction_pairs(100)

results = []

progress = st.progress(0)

total = len(pairs)

for count, (_, row) in enumerate(pairs.iterrows(), start=1):

    signal = detector.calculate_signal(
        row["drugname"],
        row["pt"]
    )

    if signal is not None:
        results.append(signal)

    progress.progress(count / total)

progress.empty()

ranking = pd.DataFrame(results)

if ranking.empty:
    st.warning("No signals were calculated.")
    st.stop()

ranking = ranking.sort_values(
    by="PRR",
    ascending=False
).reset_index(drop=True)

Path("data/processed").mkdir(
    parents=True,
    exist_ok=True
)

ranking.to_csv(
    "data/processed/signal_ranking.csv",
    index=False
)

ranking.insert(
    0,
    "Rank",
    range(1, len(ranking) + 1)
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Signals",
    len(ranking)
)

col2.metric(
    "Highest PRR",
    round(ranking["PRR"].max(), 2)
)

col3.metric(
    "Highest ROR",
    round(ranking["ROR"].max(), 2)
)

st.markdown("---")

search = st.text_input(
    "🔍 Search Drug or Reaction"
)

if search:

    ranking = ranking[
        ranking["Drug"].str.contains(search.upper(), na=False) |
        ranking["Reaction"].str.contains(search.upper(), na=False)
    ]

minimum_prr = st.slider(
    "Minimum PRR",
    1.0,
    float(ranking["PRR"].max()),
    2.0,
    0.1
)

ranking = ranking[
    ranking["PRR"] >= minimum_prr
]

st.markdown("---")

fig = px.scatter(
    ranking,
    x="PRR",
    y="ROR",
    color="Signal",
    hover_data=["Drug", "Reaction"],
    size="PRR",
    title="Signal Distribution"
)

fig.update_layout(
    template="plotly_dark",
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

display = ranking.copy()

display["Signal"] = display["Signal"].replace({
    "🔴 Strong": "🔴 Strong",
    "🟡 Moderate": "🟡 Moderate",
    "🟢 Weak": "🟢 Weak",
    "⚪ No Signal": "⚪ No Signal"
})

st.subheader("Top Drug-Reaction Signals")

st.dataframe(
    display,
    hide_index=True,
    use_container_width=True,
    height=650,
    column_config={
        "Rank": st.column_config.NumberColumn(
            "Rank",
            width=60
        ),
        "Drug": st.column_config.TextColumn(
            "Drug",
            width="medium"
        ),
        "Reaction": st.column_config.TextColumn(
            "Reaction",
            width="large"
        ),
        "PRR": st.column_config.NumberColumn(
            "PRR",
            format="%.3f"
        ),
        "ROR": st.column_config.NumberColumn(
            "ROR",
            format="%.3f"
        ),
        "Signal": st.column_config.TextColumn(
            "Signal",
            width="small"
        )
    }
)

csv = ranking.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Signal Ranking",
    csv,
    "signalqube_signal_ranking.csv",
    "text/csv"
)