import pandas as pd
import streamlit as st


@st.cache_data
def load_demo():
    return pd.read_csv(
        "data/processed/demo_clean.csv",
        low_memory=False
    )


@st.cache_data
def load_drug():
    df = pd.read_csv(
        "data/processed/drug_clean.csv",
        low_memory=False
    )

    df = df.dropna(subset=["drugname"])
    df["drugname"] = df["drugname"].str.strip().str.upper()

    return df


@st.cache_data
def load_reaction():
    df = pd.read_csv(
        "data/processed/reac_clean.csv",
        low_memory=False
    )

    df = df.dropna(subset=["pt"])
    df["pt"] = df["pt"].str.strip().str.upper()

    return df


@st.cache_data
def load_outcome():
    return pd.read_csv(
        "data/processed/outc_clean.csv",
        low_memory=False
    )