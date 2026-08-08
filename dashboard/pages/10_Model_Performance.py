import streamlit as st
import joblib
from pathlib import Path


st.set_page_config(
    page_title="Model Performance",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 SignalQUBE ML Model Performance")
st.markdown(
    "Machine Learning model used for pharmacovigilance signal classification."
)

st.divider()


# --------------------------------------------------
# MODEL METRICS
# --------------------------------------------------

st.subheader("📊 Model Performance")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Accuracy", "96.95%")
col2.metric("Precision", "99.79%")
col3.metric("Recall", "95.62%")
col4.metric("F1 Score", "97.66%")
col5.metric("ROC-AUC", "99.65%")


st.divider()


# --------------------------------------------------
# MODEL INFORMATION
# --------------------------------------------------

st.subheader("🧠 Model Information")

col1, col2 = st.columns(2)

with col1:

    st.write("**Algorithm:** Logistic Regression")
    st.write("**Training dataset:** FAERS 2025 Q4")
    st.write("**Features:** 8")
    st.write("**Target:** Signal / No Signal")


with col2:

    st.write("**Training split:** 80%")
    st.write("**Testing split:** 20%")
    st.write("**Feature scaling:** StandardScaler")
    st.write("**Random state:** 42")


st.divider()


# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

MODEL_FILE = Path("src/ml/signal_model.pkl")
SCALER_FILE = Path("src/ml/scaler.pkl")

try:

    model = joblib.load(MODEL_FILE)
    scaler = joblib.load(SCALER_FILE)

    st.success("✅ Logistic Regression model loaded successfully.")

except Exception as e:

    st.error(
        f"Unable to load ML model: {e}"
    )

    st.stop()


# --------------------------------------------------
# ML PREDICTOR
# --------------------------------------------------

st.subheader("🔬 ML Signal Predictor")

st.write(
    "Enter statistical signal metrics to obtain an ML classification."
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    A = st.number_input(
        "A — Drug + Reaction",
        min_value=0,
        value=10
    )

with col2:
    B = st.number_input(
        "B — Drug Only",
        min_value=0,
        value=20
    )

with col3:
    C = st.number_input(
        "C — Reaction Only",
        min_value=0,
        value=30
    )

with col4:
    D = st.number_input(
        "D — Neither",
        min_value=0,
        value=385000
    )


col1, col2, col3, col4 = st.columns(4)

with col1:
    PRR = st.number_input(
        "PRR",
        min_value=0.0,
        value=5.0
    )

with col2:
    ROR = st.number_input(
        "ROR",
        min_value=0.0,
        value=10.0
    )

with col3:
    ChiSquare = st.number_input(
        "Chi-Square",
        value=25.0
    )

with col4:
    ROR_Lower95 = st.number_input(
        "ROR Lower 95%",
        value=2.0
    )


if st.button(
    "🚀 Predict Signal",
    type="primary"
):

    features = [[
        A,
        B,
        C,
        D,
        PRR,
        ROR,
        ChiSquare,
        ROR_Lower95
    ]]

    scaled_features = scaler.transform(
        features
    )

    prediction = model.predict(
        scaled_features
    )[0]

    probability = model.predict_proba(
        scaled_features
    )[0][1]

    st.divider()

    if prediction == 1:

        st.success(
            "🔴 Signal Detected"
        )

    else:

        st.info(
            "🟢 No Signal"
        )

    st.metric(
        "ML Signal Probability",
        f"{probability * 100:.2f}%"
    )