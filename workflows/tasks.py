from prefect import task
import subprocess


@task(name="Load & Clean Data")
def preprocess_data():
    print("Running preprocessing...")

    subprocess.run(
        ["python", "src/preprocessing/preprocess.py"],
        check=True
    )


@task(name="Merge Data")
def merge_data():
    print("Running merge...")

    subprocess.run(
        ["python", "src/preprocessing/merge_data.py"],
        check=True
    )


@task(name="Signal Detection")
def signal_detection():
    print("Running signal detection...")

    subprocess.run(
        ["python", "src/analysis/test_signal_detection.py"],
        check=True
    )


@task(name="Prepare ML Dataset")
def prepare_dataset():
    print("Preparing ML dataset...")

    subprocess.run(
        ["python", "src/ml/prepare_dataset.py"],
        check=True
    )


@task(name="Train ML Model")
def train_model():
    print("Training ML model...")

    subprocess.run(
        ["python", "src/ml/train_model.py"],
        check=True
    )


@task(name="Generate Report")
def generate_report():
    print("Generating report...")

    subprocess.run(
        ["python", "src/reports/report_generator.py"],
        check=True
    )