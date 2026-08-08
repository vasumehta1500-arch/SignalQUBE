import streamlit as st
import pandas as pd


@st.cache_data
def load_demo():
    return pd.read_csv(
        "data/sample/demo_clean.csv",
        low_memory=False
    )


@st.cache_data
def load_drug():
    return pd.read_csv(
        "data/sample/drug_clean.csv",
        low_memory=False
    )


@st.cache_data
def load_reaction():
    return pd.read_csv(
        "data/sample/reac_clean.csv",
        low_memory=False
    )


@st.cache_data
def load_outcome():
    return pd.read_csv(
        "data/sample/outc_clean.csv",
        low_memory=False
    )