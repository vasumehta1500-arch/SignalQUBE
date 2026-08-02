import streamlit as st
import tempfile
from pathlib import Path
import pandas as pd

from data_loader import (
    load_drug,
    load_reaction
)

from reports.report_generator import generate_report

st.set_page_config(
    page_title="Report Generator",
    page_icon="📄",
    layout="wide"
)

st.title("📄 SignalQUBE Report Generator")

drug = load_drug()
reaction = load_reaction()

stats = {

    "drug_records": len(drug),

    "reaction_records": len(reaction),

    "unique_drugs": drug["drugname"].nunique(),

    "unique_reactions": reaction["pt"].nunique()

}

ranking_file = Path(
    "data/processed/signal_ranking.csv"
)

if ranking_file.exists():

    ranking = pd.read_csv(ranking_file)

else:

    ranking = pd.DataFrame(
        columns=[
            "Drug",
            "Reaction",
            "PRR",
            "ROR",
            "Signal"
        ]
    )

st.markdown("---")

col1, col2 = st.columns(2)

col1.metric(
    "📊 Unique Drugs",
    stats["unique_drugs"]
)

col2.metric(
    "🏆 Saved Signals",
    len(ranking)
)

st.markdown("---")

if st.button("📄 Generate Professional Report"):

    with st.spinner("Generating PDF..."):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as tmp:

            generate_report(
                stats,
                ranking,
                tmp.name
            )

            with open(
                tmp.name,
                "rb"
            ) as file:

                pdf = file.read()

    st.success("✅ Report Generated Successfully!")

    st.download_button(
        label="⬇ Download SignalQUBE Report",
        data=pdf,
        file_name="SignalQUBE_Report.pdf",
        mime="application/pdf"
    )