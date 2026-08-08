import streamlit as st
from pathlib import Path
import sys


# Add dashboard folder to Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils import load_signals


st.set_page_config(
    page_title="SignalQUBE",
    page_icon="🧬",
    layout="wide"
)


# -----------------------------
# Load Deployment Data
# -----------------------------

signals = load_signals()


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
    "📄 FAERS Cases",
    "385,288"
)

col2.metric(
    "💊 Drug Records",
    "1,814,314"
)

col3.metric(
    "⚠ Reaction Records",
    "1,332,835"
)

col4.metric(
    "🔬 Signal Pairs",
    "285,912"
)

st.markdown("---")


# -----------------------------
# Deployment Dataset
# -----------------------------

st.subheader("🚀 Deployed Analysis Dataset")

st.info(
    f"""
The deployed dashboard contains **{len(signals):,} selected signal pairs**
derived from the full FDA FAERS 2025 Q4 dataset.

The complete FAERS dataset is used locally for dissertation-level
preprocessing and statistical analysis.
"""
)


# -----------------------------
# Technology Stack
# -----------------------------

st.subheader("🛠 Technology Stack")

tech1, tech2, tech3 = st.columns(3)

with tech1:
    st.success("""
**Python**

Pandas

NumPy

Scikit-learn
""")

with tech2:
    st.info("""
**Streamlit**

Plotly

Joblib

CSV Processing
""")

with tech3:
    st.warning("""
**Pharmacovigilance**

PRR

ROR

Logistic Regression
""")


st.markdown("---")


# -----------------------------
# Workflow Automation
# -----------------------------

st.subheader("⚙️ Workflow Automation")

st.success("""
SignalQUBE uses **Prefect** to automate:

- Data Validation
- Dataset Preparation
- Machine Learning Training
- Signal Detection Testing
""")


# -----------------------------
# Workflow
# -----------------------------

st.subheader("🔄 SignalQUBE Workflow")

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

# -----------------------------
# Workflow
# -----------------------------

st.markdown("---")

st.subheader("⚙️ Workflow Automation")

st.success(
    """
SignalQUBE uses Prefect to automate:

- Data Validation
- Dataset Preparation
- Machine Learning Training
- Signal Detection Testing

This reduces manual execution and provides a reproducible workflow.
"""
)

st.subheader("🔄 SignalQUBE Workflow")

st.code(
    """
FAERS Dataset
      |
      v
Data Cleaning
      |
      v
Drug + Reaction Merge
      |
      v
Signal Detection
(PRR / ROR)
      |
      v
Machine Learning
(Logistic Regression)
      |
      v
AI Prediction
      |
      v
Signal Comparison
      |
      v
CSV / PDF Reports
""",
    language="text"
)