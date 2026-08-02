import pandas as pd
from pathlib import Path
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# ---------------------------------------
# Load Training Dataset
# ---------------------------------------

data_path = Path(__file__).parent / "training_data.csv"

df = pd.read_csv(data_path)

print("=" * 60)
print("Training Dataset Loaded")
print(df.head())
print("=" * 60)

# ---------------------------------------
# Features & Target
# ---------------------------------------

X = df[["A", "B", "C", "D", "PRR", "ROR"]]
y = df["Label"]

# ---------------------------------------
# Train-Test Split
# ---------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ---------------------------------------
# Train Model
# ---------------------------------------

model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)

# ---------------------------------------
# Prediction
# ---------------------------------------

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

print("\nAccuracy :", round(accuracy * 100, 2), "%")
print("Precision:", round(precision * 100, 2), "%")
print("Recall   :", round(recall * 100, 2), "%")
print("F1 Score :", round(f1 * 100, 2), "%")

print("\nConfusion Matrix")
print(cm)

print("\nClassification Report")
print(classification_report(y_test, y_pred))

# ---------------------------------------
# Save ML Model
# ---------------------------------------

model_path = Path(__file__).parent / "signal_model.pkl"

joblib.dump(model, model_path)

print("\nModel Saved Successfully")
print(model_path)

# ---------------------------------------
# Save Model Metrics
# ---------------------------------------

metrics = {
    "Accuracy": accuracy,
    "Precision": precision,
    "Recall": recall,
    "F1": f1,
    "ConfusionMatrix": cm
}

metrics_path = Path(__file__).parent / "model_metrics.pkl"

joblib.dump(metrics, metrics_path)

print("\nModel Metrics Saved Successfully")
print(metrics_path)

print("\nTraining Completed Successfully.")