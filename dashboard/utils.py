import pandas as pd
import streamlit as st


DEPLOYMENT_FILE = "data/deployment/signal_results.csv"


@st.cache_data
def load_signals():
    """
    Load the deployment signal dataset.
    """
    df = pd.read_csv(
        DEPLOYMENT_FILE,
        low_memory=False
    )

    if "drugname" in df.columns:
        df["drugname"] = (
            df["drugname"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

    if "pt" in df.columns:
        df["pt"] = (
            df["pt"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

    return df


@st.cache_data
def load_demo():
    """
    Deployment-safe summary representing FAERS reports.
    """
    return pd.DataFrame({
        "dataset": ["DEMO"],
        "records": [385288]
    })


@st.cache_data
def load_drug():
    """
    Load signal dataset for dashboard drug analysis.
    """
    return load_signals()


@st.cache_data
def load_reaction():
    """
    Load signal dataset for dashboard reaction analysis.
    """
    return load_signals()


@st.cache_data
def load_outcome():
    """
    Deployment-safe summary representing FAERS outcomes.
    """
    return pd.DataFrame({
        "dataset": ["OUTC"],
        "records": [289721]
    })