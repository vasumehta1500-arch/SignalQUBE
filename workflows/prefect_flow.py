from prefect import flow, task
import subprocess
import time


@task(name="Prepare Dataset")
def prepare_dataset():
    print("Preparing ML Dataset...")
    subprocess.run(
        ["python", "src/ml/prepare_dataset.py"],
        check=True
    )


@task(name="Train AI Model")
def train_model():
    print("Training Logistic Regression Model...")
    subprocess.run(
        ["python", "src/ml/train_model.py"],
        check=True
    )


@task(name="Validate Data")
def validate_data():
    print("Validating Processed Data...")
    subprocess.run(
        ["python", "src/validate_data.py"],
        check=True
    )


@task(name="Signal Detection Test")
def signal_test():
    print("Testing Signal Detection...")
    subprocess.run(
        ["python", "src/test_signal_detection.py"],
        check=True
    )


@flow(name="SignalQUBE Workflow")
def signalqube_pipeline():

    print("=" * 60)
    print("SignalQUBE Workflow Started")
    print("=" * 60)

    validate_data()

    prepare_dataset()

    train_model()

    signal_test()

    print("=" * 60)
    print("Workflow Completed Successfully")
    print("=" * 60)


if __name__ == "__main__":
    signalqube_pipeline()