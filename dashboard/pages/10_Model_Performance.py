import streamlit as st
import joblib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="Model Performance",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Load Metrics
# -----------------------------

metrics_path = Path("src/ml/model_metrics.pkl")

metrics = joblib.load(metrics_path)

# -----------------------------
# Title
# -----------------------------

st.title("🤖 Machine Learning Model Performance")

st.write(
    "Performance evaluation of the Logistic Regression model used for AI-based signal prediction."
)

st.markdown("---")

# -----------------------------
# Metrics
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Accuracy",
    f"{metrics['Accuracy']*100:.2f}%"
)

col2.metric(
    "Precision",
    f"{metrics['Precision']*100:.2f}%"
)

col3.metric(
    "Recall",
    f"{metrics['Recall']*100:.2f}%"
)

col4.metric(
    "F1 Score",
    f"{metrics['F1']*100:.2f}%"
)

st.markdown("---")

# -----------------------------
# Confusion Matrix
# -----------------------------

st.subheader("📊 Confusion Matrix")

cm = metrics["ConfusionMatrix"]

cm_df = pd.DataFrame(
    cm,
    columns=[
        "Predicted Negative",
        "Predicted Positive"
    ],
    index=[
        "Actual Negative",
        "Actual Positive"
    ]
)

fig_cm = px.imshow(
    cm_df,
    text_auto=True,
    color_continuous_scale="Blues",
    title="Confusion Matrix"
)

st.plotly_chart(
    fig_cm,
    use_container_width=True
)

st.markdown("---")

# -----------------------------
# Performance Chart
# -----------------------------

performance = pd.DataFrame({
    "Metric":[
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score"
    ],
    "Value":[
        metrics["Accuracy"]*100,
        metrics["Precision"]*100,
        metrics["Recall"]*100,
        metrics["F1"]*100
    ]
})

fig_bar = px.bar(
    performance,
    x="Metric",
    y="Value",
    text="Value",
    color="Metric",
    title="Model Performance"
)

fig_bar.update_traces(
    texttemplate="%{y:.2f}%",
    textposition="outside"
)

fig_bar.update_layout(
    template="plotly_dark",
    height=500,
    showlegend=False,
    yaxis_title="Percentage"
)

st.plotly_chart(
    fig_bar,
    use_container_width=True
)

st.markdown("---")

# -----------------------------
# Accuracy Gauge
# -----------------------------

st.subheader("🎯 Model Accuracy Gauge")

gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=metrics["Accuracy"]*100,
        title={"text":"Accuracy"},
        gauge={
            "axis":{"range":[0,100]},
            "bar":{"color":"green"},
            "steps":[
                {"range":[0,60],"color":"#ffb3b3"},
                {"range":[60,80],"color":"#ffe699"},
                {"range":[80,100],"color":"#b6fcb6"}
            ]
        }
    )
)

gauge.update_layout(
    template="plotly_dark",
    height=450
)

st.plotly_chart(
    gauge,
    use_container_width=True
)

st.markdown("---")

st.success(
    f"""
Model trained successfully.

Accuracy : {metrics['Accuracy']*100:.2f}%

This model is used by SignalQUBE to predict the signal strength of drug-reaction pairs using Machine Learning.
"""
)