import streamlit as st
import pandas as pd
import sys
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.analysis.signal_detection import SignalDetector
from src.ml.predict_model import predict_signal

st.set_page_config(
    page_title="Signal Comparison",
    page_icon="⚖️",
    layout="wide"
)

@st.cache_resource
def get_detector():
    return SignalDetector()

detector = get_detector()

merged = detector.prepare_data()

drug_list = sorted(merged["drugname"].dropna().unique())
reaction_list = sorted(merged["pt"].dropna().unique())

st.title("⚖️ Signal Comparison")
st.subheader("Traditional Pharmacovigilance vs AI Prediction")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    selected_drug = st.selectbox(
        "💊 Select Drug",
        drug_list
    )

with col2:
    selected_reaction = st.selectbox(
        "⚠️ Select Reaction",
        reaction_list
    )

st.markdown("")

if st.button("🚀 Compare Methods", use_container_width=True):

    result = detector.calculate_signal(
        selected_drug,
        selected_reaction
    )

    # -----------------------------
    # Handle No Signal
    # -----------------------------

    if result["PRR"] is None:

        st.warning("No statistical signal found.")

        st.stop()

    prediction = predict_signal(
        result["A"],
        result["B"],
        result["C"],
        result["D"],
        result["PRR"],
        result["ROR"]
    )

    st.success("Comparison Completed Successfully")

    st.markdown("---")

    st.header("Traditional Signal Detection")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "PRR",
        result["PRR"]
    )

    c2.metric(
        "ROR",
        result["ROR"]
    )

    c3.metric(
        "Signal",
        result["Signal"]
    )

    st.markdown("---")

    st.header("Machine Learning Prediction")

    c4, c5 = st.columns(2)

    c4.metric(
        "Prediction",
        prediction["Prediction"]
    )

    c5.metric(
        "Confidence",
        f"{prediction['Confidence']} %"
    )

    st.markdown("---")

    traditional = result["Signal"]
    ai = prediction["Prediction"]

    if "Strong" in traditional and "Strong" in ai:

        agreement = "✅ Both methods agree"

    elif "Weak" in traditional and "Weak" in ai:

        agreement = "✅ Both methods agree"

    elif "Moderate" in traditional and "Strong" in ai:

        agreement = "⚠ AI predicts a stronger signal"

    elif "Strong" in traditional and "Weak" in ai:

        agreement = "⚠ AI predicts a weaker signal"

    else:

        agreement = "⚠ Methods disagree"

    st.header("Comparison Result")

    st.info(agreement)

    if "agree" in agreement.lower():

        st.success(
            """
Traditional pharmacovigilance and Machine Learning
both reached the same conclusion.

This increases confidence in the signal.
"""
        )

    else:

        st.warning(
            """
The statistical method and Machine Learning
produced different results.

Clinical review is recommended.
"""
        )

    st.markdown("---")

    comparison = pd.DataFrame({

        "Metric":[
            "Drug",
            "Reaction",
            "PRR",
            "ROR",
            "Traditional Signal",
            "AI Prediction",
            "Confidence",
            "Agreement"
        ],

        "Traditional":[
            result["Drug"],
            result["Reaction"],
            result["PRR"],
            result["ROR"],
            result["Signal"],
            "-",
            "-",
            agreement
        ],

        "Machine Learning":[
            result["Drug"],
            result["Reaction"],
            "-",
            "-",
            prediction["Prediction"],
            prediction["Prediction"],
            f"{prediction['Confidence']} %",
            agreement
        ]

    })

  
    st.subheader("Comparison Table")

    st.dataframe(
        comparison,
        hide_index=True,
        use_container_width=True
    )

    csv = comparison.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Comparison Report",
        csv,
        "signal_comparison.csv",
        "text/csv"
    )

    st.markdown("---")
    st.subheader("📊 Traditional vs AI Analysis")

    # Prepare values
    prr = result["PRR"]
    ror = result["ROR"]
    confidence = prediction["Confidence"]

    # Create figure
    fig = go.Figure()

    # Traditional Method
    fig.add_trace(
        go.Bar(
            name="Traditional",
            x=["PRR", "ROR"],
            y=[prr, ror],
            marker_color="royalblue"
        )
    )

    # Machine Learning
    fig.add_trace(
        go.Bar(
            name="Logistic Regression",
            x=["Confidence"],
            y=[confidence],
            marker_color="orange"
        )
    )

    fig.update_layout(
        title="Traditional Statistical Method vs Logistic Regression",
        xaxis_title="Method",
        yaxis_title="Value",
        barmode="group",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

   