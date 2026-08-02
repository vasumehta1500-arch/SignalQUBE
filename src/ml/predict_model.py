from pathlib import Path
import joblib
import pandas as pd

# Load trained model once
MODEL_PATH = Path(__file__).parent / "signal_model.pkl"
model = joblib.load(MODEL_PATH)


def predict_signal(A, B, C, D, PRR, ROR):

    sample = pd.DataFrame([{
        "A": A,
        "B": B,
        "C": C,
        "D": D,
        "PRR": PRR,
        "ROR": ROR
    }])

    prediction = model.predict(sample)[0]

    probability = model.predict_proba(sample)[0]

    confidence = max(probability) * 100

    label = "🔴 Strong Signal" if prediction == 1 else "🟢 Weak Signal"

    return {
        "Prediction": label,
        "Confidence": round(confidence, 2)
    }