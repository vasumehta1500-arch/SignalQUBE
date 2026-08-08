import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)


# --------------------------------------------------
# PATHS
# --------------------------------------------------

DATA_FILE = Path(
    "src/ml/training_data.csv"
)

MODEL_FILE = Path(
    "src/ml/signal_model.pkl"
)

SCALER_FILE = Path(
    "src/ml/scaler.pkl"
)


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    print("=" * 60)
    print("SIGNALQUBE ML MODEL TRAINING")
    print("=" * 60)

    # --------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------

    print("\nLoading training dataset...")

    df = pd.read_csv(DATA_FILE)

    print(
        f"Dataset shape: {df.shape}"
    )

    # --------------------------------------------------
    # FEATURES
    # --------------------------------------------------

    feature_columns = [
        "A",
        "B",
        "C",
        "D",
        "PRR",
        "ROR",
        "ChiSquare",
        "ROR_Lower95"
    ]

    X = df[feature_columns]

    y = df["Label"]

    print("\nFeatures:")
    print(feature_columns)

    print("\nTarget distribution:")
    print(y.value_counts())

    # --------------------------------------------------
    # TRAIN / TEST SPLIT
    # --------------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    print("\nTraining samples:", len(X_train))
    print("Testing samples :", len(X_test))

    # --------------------------------------------------
    # FEATURE SCALING
    # --------------------------------------------------

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(
        X_train
    )

    X_test_scaled = scaler.transform(
        X_test
    )

    # --------------------------------------------------
    # TRAIN MODEL
    # --------------------------------------------------

    print("\nTraining Logistic Regression...")

    model = LogisticRegression(
        max_iter=1000,
        random_state=42
    )

    model.fit(
        X_train_scaled,
        y_train
    )

    # --------------------------------------------------
    # PREDICTION
    # --------------------------------------------------

    y_pred = model.predict(
        X_test_scaled
    )

    y_probability = model.predict_proba(
        X_test_scaled
    )[:, 1]

    # --------------------------------------------------
    # EVALUATION
    # --------------------------------------------------

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0
    )

    auc = roc_auc_score(
        y_test,
        y_probability
    )

    print("\n" + "=" * 60)
    print("MODEL PERFORMANCE")
    print("=" * 60)

    print(
        f"\nAccuracy  : {accuracy:.4f}"
    )

    print(
        f"Precision : {precision:.4f}"
    )

    print(
        f"Recall    : {recall:.4f}"
    )

    print(
        f"F1 Score  : {f1:.4f}"
    )

    print(
        f"ROC-AUC   : {auc:.4f}"
    )

    # --------------------------------------------------
    # CONFUSION MATRIX
    # --------------------------------------------------

    print("\nConfusion Matrix:")

    print(
        confusion_matrix(
            y_test,
            y_pred
        )
    )

    # --------------------------------------------------
    # CLASSIFICATION REPORT
    # --------------------------------------------------

    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            y_pred,
            zero_division=0
        )
    )

    # --------------------------------------------------
    # SAVE MODEL
    # --------------------------------------------------

    MODEL_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(
        model,
        MODEL_FILE
    )

    joblib.dump(
        scaler,
        SCALER_FILE
    )

    print("\nModel saved:")
    print(MODEL_FILE)

    print("\nScaler saved:")
    print(SCALER_FILE)

    print("\n" + "=" * 60)
    print("MODEL TRAINING COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()