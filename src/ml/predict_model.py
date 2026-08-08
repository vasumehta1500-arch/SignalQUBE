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

        if not MODEL_FILE.exists():
            raise FileNotFoundError(
                f"Model file not found: {MODEL_FILE}"
            )

        if not SCALER_FILE.exists():
            raise FileNotFoundError(
                f"Scaler file not found: {SCALER_FILE}"
            )

        self.model = joblib.load(MODEL_FILE)
        self.scaler = joblib.load(SCALER_FILE)

        # Features used by the ML model
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

        # Create input DataFrame
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

        # Make sure feature order matches training
        data = data[self.features]

        # Apply scaler
        data_scaled = self.scaler.transform(data)

        # ML prediction
        prediction = self.model.predict(
            data_scaled
        )[0]

        # Prediction probability
        probability = self.model.predict_proba(
            data_scaled
        )[0][1]

        # Convert prediction to readable result
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



