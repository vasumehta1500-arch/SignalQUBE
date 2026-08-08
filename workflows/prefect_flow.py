from prefect import flow, task
import subprocess
import sys
from pathlib import Path


# ---------------------------------------------------------
# 1. DOWNLOAD FDA FAERS DATA
# ---------------------------------------------------------
@task(name="Download FDA FAERS Data")
def download_faers():
    print("=" * 60)
    print("Downloading FDA FAERS Data")
    print("=" * 60)

    subprocess.run(
        [
            sys.executable,
            "src/data/download_faers.py"
        ],
        check=True
    )


# ---------------------------------------------------------
# 2. VALIDATE DATA
# ---------------------------------------------------------
@task(name="Validate Data")
def validate_data():
    print("\nValidating Processed Data...")

    subprocess.run(
        [
            sys.executable,
            "src/validate_data.py"
        ],
        check=True
    )


# ---------------------------------------------------------
# 3. PREPARE ML DATASET
# ---------------------------------------------------------
@task(name="Prepare Dataset")
def prepare_dataset():
    print("\nPreparing ML Dataset...")

    subprocess.run(
        [
            sys.executable,
            "src/ml/prepare_dataset.py"
        ],
        check=True
    )


# ---------------------------------------------------------
# 4. TRAIN AI MODEL
# ---------------------------------------------------------
@task(name="Train AI Model")
def train_model():
    print("\nTraining Logistic Regression Model...")

    subprocess.run(
        [
            sys.executable,
            "src/ml/train_model.py"
        ],
        check=True
    )


# ---------------------------------------------------------
# 5. TEST SIGNAL DETECTION
# ---------------------------------------------------------
@task(name="Signal Detection Test")
def signal_test():
    print("\nTesting Signal Detection...")

    subprocess.run(
        [
            sys.executable,
            "src/test_signal_detection.py"
        ],
        check=True
    )


# ---------------------------------------------------------
# MAIN PREFECT FLOW
# ---------------------------------------------------------
@flow(name="SignalQUBE FDA Research Pipeline")
def signalqube_pipeline():

    print("=" * 60)
    print("SIGNALQUBE FDA RESEARCH PIPELINE")
    print("=" * 60)

    # Step 1
    download_faers()

    # Step 2
    validate_data()

    # Step 3
    prepare_dataset()

    # Step 4
    train_model()

    # Step 5
    signal_test()

    print("=" * 60)
    print("SIGNALQUBE PIPELINE COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    signalqube_pipeline()