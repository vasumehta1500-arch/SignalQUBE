import streamlit as st
import pandas as pd
import sys
import plotly.graph_objects as go
from pathlib import Path


# ==================================================
# PROJECT PATH
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))


# ==================================================
# IMPORTS
# ==================================================

from src.analysis.signal_detection import SignalDetector
from src.ml.predict_model import predict_signal


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Signal Comparison",
    page_icon="⚖️",
    layout="wide"
)


# ==================================================
# LOAD SIGNAL DETECTOR
# ==================================================

@st.cache_resource
def get_detector():
    return SignalDetector()


detector = get_detector()


# ==================================================
# PREPARE DATA
# ==================================================

merged = detector.prepare_data()

drug_list = sorted(
    merged["drugname"]
    .dropna()
    .unique()
)

reaction_list = sorted(
    merged["pt"]
    .dropna()
    .unique()
)


# ==================================================
# PAGE TITLE
# ==================================================

st.title("⚖️ Signal Comparison")

st.subheader(
    "Traditional Pharmacovigilance vs AI Prediction"
)

st.markdown("---")


# ==================================================
# SELECT DRUG AND REACTION
# ==================================================

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


# ==================================================
# COMPARE METHODS
# ==================================================

if st.button(
    "🚀 Compare Methods",
    use_container_width=True
):

    # --------------------------------------------------
    # TRADITIONAL SIGNAL
    # --------------------------------------------------

    result = detector.calculate_signal(
        selected_drug,
        selected_reaction
    )


    # --------------------------------------------------
    # HANDLE NO STATISTICAL RESULT
    # --------------------------------------------------

    if result["PRR"] is None:

        st.warning(
            "No statistical signal found for the "
            "selected drug and reaction."
        )

        st.stop()


    # ==================================================
    # MACHINE LEARNING PREDICTION
    # ==================================================

    prediction = predict_signal(
        A=result["A"],
        B=result["B"],
        C=result["C"],
        D=result["D"],
        PRR=result["PRR"],
        ROR=result["ROR"],
        ChiSquare=result["ChiSquare"],
        ROR_Lower95=result["ROR_Lower95"]
    )


    # --------------------------------------------------
    # ML VALUES
    # --------------------------------------------------

    ml_raw_prediction = prediction["Prediction"]

    confidence = prediction["Probability"]


    # --------------------------------------------------
    # CONVERT ML RESULT TO READABLE LABEL
    # --------------------------------------------------

    if ml_raw_prediction == 1:

        if confidence >= 75:

            ai_prediction = "Strong Signal"

        elif confidence >= 50:

            ai_prediction = "Moderate Signal"

        else:

            ai_prediction = "Weak Signal"

    else:

        ai_prediction = "No Signal"


    # ==================================================
    # SUCCESS
    # ==================================================

    st.success(
        "Comparison Completed Successfully"
    )


    st.markdown("---")


    # ==================================================
    # TRADITIONAL METHOD
    # ==================================================

    st.header(
        "Traditional Signal Detection"
    )

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


    # ==================================================
    # MACHINE LEARNING
    # ==================================================

    st.header(
        "Machine Learning Prediction"
    )

    c4, c5 = st.columns(2)

    c4.metric(
        "Prediction",
        ai_prediction
    )

    c5.metric(
        "Confidence",
        f"{confidence} %"
    )


    st.markdown("---")


    # ==================================================
    # NORMALIZE TRADITIONAL SIGNAL
    # ==================================================

    traditional = result["Signal"]

    if "Strong" in traditional:

        traditional_level = "Strong"

    elif "Moderate" in traditional:

        traditional_level = "Moderate"

    elif "Weak" in traditional:

        traditional_level = "Weak"

    else:

        traditional_level = "No Signal"


    # ==================================================
    # NORMALIZE AI SIGNAL
    # ==================================================

    if ai_prediction == "Strong Signal":

        ai_level = "Strong"

    elif ai_prediction == "Moderate Signal":

        ai_level = "Moderate"

    elif ai_prediction == "Weak Signal":

        ai_level = "Weak"

    else:

        ai_level = "No Signal"


    # ==================================================
    # COMPARE METHODS
    # ==================================================

    if traditional_level == ai_level:

        agreement = "✅ Both methods agree"

    elif (
        traditional_level == "Strong"
        and ai_level in ["Moderate", "Weak", "No Signal"]
    ):

        agreement = "⚠ AI predicts a weaker signal"

    elif (
        traditional_level in ["Weak", "No Signal"]
        and ai_level == "Strong"
    ):

        agreement = "⚠ AI predicts a stronger signal"

    else:

        agreement = "⚠ Methods disagree"


    # ==================================================
    # COMPARISON RESULT
    # ==================================================

    st.header(
        "Comparison Result"
    )

    st.info(
        agreement
    )


    if "Both methods agree" in agreement:

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


    # ==================================================
    # ML DEBUG INFORMATION
    # ==================================================

    with st.expander(
        "🔍 View ML Details"
    ):

        st.write(
            "Raw ML Prediction:",
            ml_raw_prediction
        )

        st.write(
            "ML Probability:",
            f"{confidence} %"
        )

        st.write(
            "Traditional Signal:",
            result["Signal"]
        )

        st.write(
            "A:",
            result["A"]
        )

        st.write(
            "B:",
            result["B"]
        )

        st.write(
            "C:",
            result["C"]
        )

        st.write(
            "D:",
            result["D"]
        )

        st.write(
            "PRR:",
            result["PRR"]
        )

        st.write(
            "ROR:",
            result["ROR"]
        )

        st.write(
            "Chi-Square:",
            result["ChiSquare"]
        )

        st.write(
            "ROR Lower 95%:",
            result["ROR_Lower95"]
        )


    st.markdown("---")


    # ==================================================
    # COMPARISON TABLE
    # ==================================================

    comparison = pd.DataFrame({

        "Metric": [

            "Drug",
            "Reaction",
            "A",
            "B",
            "C",
            "D",
            "PRR",
            "ROR",
            "Chi-Square",
            "ROR Lower 95%",
            "Traditional Signal",
            "AI Prediction",
            "AI Confidence",
            "Agreement"

        ],

        "Traditional": [

            result["Drug"],
            result["Reaction"],
            result["A"],
            result["B"],
            result["C"],
            result["D"],
            result["PRR"],
            result["ROR"],
            result["ChiSquare"],
            result["ROR_Lower95"],
            result["Signal"],
            "-",
            "-",
            agreement

        ],

        "Machine Learning": [

            result["Drug"],
            result["Reaction"],
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            ai_prediction,
            f"{confidence} %",
            agreement

        ]

    })


    st.subheader(
        "Comparison Table"
    )

    st.dataframe(
        comparison,
        hide_index=True,
        use_container_width=True
    )


    # ==================================================
    # DOWNLOAD REPORT
    # ==================================================

    csv = comparison.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(
        "📥 Download Comparison Report",
        csv,
        "signal_comparison.csv",
        "text/csv"
    )


    st.markdown("---")


    # ==================================================
    # CHART
    # ==================================================

    st.subheader(
        "📊 Traditional vs AI Analysis"
    )


    prr = result["PRR"]

    ror = result["ROR"]

    confidence = prediction["Probability"]


    # --------------------------------------------------
    # CREATE CHART
    # --------------------------------------------------

    fig = go.Figure()


    # Traditional PRR

    fig.add_trace(
        go.Bar(
            name="PRR",
            x=["Traditional"],
            y=[prr]
        )
    )


    # Traditional ROR

    fig.add_trace(
        go.Bar(
            name="ROR",
            x=["Traditional"],
            y=[ror]
        )
    )


    # AI Confidence

    fig.add_trace(
        go.Bar(
            name="AI Confidence",
            x=["Machine Learning"],
            y=[confidence]
        )
    )


    # --------------------------------------------------
    # CHART LAYOUT
    # --------------------------------------------------

    fig.update_layout(

        title=(
            "Traditional Statistical Method "
            "vs Logistic Regression"
        ),

        xaxis_title="Method",

        yaxis_title="Value",

        barmode="group",

        height=500

    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

