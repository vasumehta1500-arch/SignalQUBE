import streamlit as st

st.set_page_config(
    page_title="SignalQUBE",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 SignalQUBE")
st.subheader("AI-Powered Pharmacovigilance Signal Detection System")

st.success("Welcome to SignalQUBE!")

st.markdown(
    """
Select a page from the sidebar to begin exploring the FAERS dataset.

### Available Modules

- 🏠 Home
- 💊 Drug Analysis
- ⚠️ Reaction Analysis
- 📈 Signal Detection
- 📊 Statistics
- 📥 Reports
- ℹ️ About
"""
)