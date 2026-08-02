import streamlit as st
import pandas as pd
from pathlib import Path
import sys



sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils import (
    load_demo,
    load_drug,
    load_reaction,
    load_outcome
)

st.set_page_config(
    page_title="SignalQUBE",
    page_icon="🧬",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------

@st.cache_data
def load_data():
    demo = load_demo()
    drug = load_drug()
    reac = load_reaction()
    outc = load_outcome()
    return demo, drug, reac, outc

demo, drug, reac, outc = load_data()

# -----------------------------
# Header
# -----------------------------

st.title("🧬 SignalQUBE")

st.markdown("""
### AI-Powered Pharmacovigilance Signal Detection System

Using **FAERS**, **Machine Learning**, **PRR**, and **ROR**
to identify potential adverse drug reaction signals.
""")

st.markdown("---")

# -----------------------------
# Dataset Statistics
# -----------------------------

st.subheader("📊 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "📄 Cases",
    f"{len(demo):,}"
)

col2.metric(
    "💊 Drug Records",
    f"{len(drug):,}"
)

col3.metric(
    "⚠ Reaction Records",
    f"{len(reac):,}"
)

col4.metric(
    "🏥 Outcome Records",
    f"{len(outc):,}"
)

st.markdown("---")

# -----------------------------
# Technology Stack
# -----------------------------

st.subheader("🛠 Technology Stack")

tech1, tech2, tech3 = st.columns(3)

with tech1:
    st.success("""
Python

Pandas

NumPy

Scikit-learn
""")

with tech2:
    st.info("""
Streamlit

Plotly

Joblib

CSV Processing
""")

with tech3:
    st.warning("""
Machine Learning

Logistic Regression

PRR

ROR
""")

st.markdown("---")

# -----------------------------
# Workflow
# -----------------------------
st.markdown("---")

st.subheader("⚙️ Workflow Automation")

st.success("""
SignalQUBE uses **Prefect** to automate:

- Data Validation
- Dataset Preparation
- Machine Learning Training
- Signal Detection Testing

This reduces manual execution and provides a reproducible workflow.
""")

st.subheader("🔄 SignalQUBE Workflow")

st.markdown("""
```text
FAERS Dataset
      │
      ▼
Data Cleaning
      │
      ▼
Drug + Reaction Merge
      │
      ▼
Signal Detection
(PRR / ROR)
      │
      ▼
Machine Learning
(Logistic Regression)
      │
      ▼
AI Prediction
      │
      ▼
Signal Comparison
      │
      ▼
CSV / PDF Reports
""")