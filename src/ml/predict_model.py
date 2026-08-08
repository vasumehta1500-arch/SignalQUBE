import joblib
import pandas as pd
from pathlib import Path


# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_FILE = PROJECT_ROOT / "src" / "ml" / "signal_model.pkl"
SCALER_FILE = PROJECT_ROOT / "src" / "ml" / "scaler.pkl"


# --------------------------------------------------
# SIGNAL PREDICTOR
# --------------------------------------------------

class SignalPredictor:

    def __init__(self):

        print("Loading ML model...")

        self.model = joblib.load(MODEL_FILE)
        self.scaler = joblib.load(SCALER_FILE)

        self.features = [
            "A",
            "B",
            "C",
            "D",
            "PRR",
            "ROR",
            "ChiSquare",
            "ROR_Lower95"
        ]

    # --------------------------------------------------
    # PREDICT
    # --------------------------------------------------

    def predict(
        self,
        A,
        B,
        C,
        D,
        PRR,
        ROR,
        ChiSquare,
        ROR_Lower95
    ):

        data = pd.DataFrame([{
            "A": A,
            "B": B,
            "C": C,
            "D": D,
            "PRR": PRR,
            "ROR": ROR,
            "ChiSquare": ChiSquare,
            "ROR_Lower95": ROR_Lower95
        }])

        # Make sure feature order is identical
        # to the training dataset
        data = data[self.features]

        # Apply scaler
        data_scaled = self.scaler.transform(data)

        # ML prediction
        prediction = self.model.predict(
            data_scaled
        )[0]

        # Probability
        probability = self.model.predict_proba(
            data_scaled
        )[0][1]

        if prediction == 1:
            result = "🔴 Signal Detected"
        else:
            result = "🟢 No Signal"

        return {
            "Prediction": int(prediction),
            "Probability": round(
                float(probability) * 100,
                2
            ),
            "Result": result
        }


# --------------------------------------------------
# DASHBOARD COMPATIBILITY FUNCTION
# --------------------------------------------------

def predict_signal(
    A,
    B,
    C,
    D,
    PRR,
    ROR,
    ChiSquare,
    ROR_Lower95
):
    """
    Compatibility wrapper used by the Streamlit dashboard.

    Calls SignalPredictor internally.
    """

    predictor = SignalPredictor()

    return predictor.predict(
        A=A,
        B=B,
        C=C,
        D=D,
        PRR=PRR,
        ROR=ROR,
        ChiSquare=ChiSquare,
        ROR_Lower95=ROR_Lower95
    )


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    predictor = SignalPredictor()

    result = predictor.predict(
        A=10,
        B=20,
        C=30,
        D=385000,
        PRR=5,
        ROR=10,
        ChiSquare=25,
        ROR_Lower95=2
    )

    print("\nML Prediction")
    print("=" * 40)

    for key, value in result.items():
        print(f"{key}: {value}")