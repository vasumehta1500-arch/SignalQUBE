import pandas as pd
from pathlib import Path


SOURCE = Path("data/processed/demo_clean.csv")
OUTPUT = Path("data/deployment/demo_summary.csv")

print("Loading DEMO dataset...")

demo = pd.read_csv(
    SOURCE,
    low_memory=False
)

print("Original columns:")
print(demo.columns.tolist())


# Keep only fields needed by the dashboard
columns = [
    "primaryid",
    "sex",
    "age",
    "age_cod",
    "reporter_country"
]

available = [
    col for col in columns
    if col in demo.columns
]

demo_small = demo[available].copy()


# Clean SEX
if "sex" in demo_small.columns:
    demo_small["sex"] = (
        demo_small["sex"]
        .astype(str)
        .str.strip()
        .str.upper()
    )


# Clean country
if "reporter_country" in demo_small.columns:
    demo_small["reporter_country"] = (
        demo_small["reporter_country"]
        .astype(str)
        .str.strip()
        .str.upper()
    )


# Save
OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True
)

demo_small.to_csv(
    OUTPUT,
    index=False
)

print("\nDeployment demographic dataset created.")
print(f"Rows: {len(demo_small):,}")
print(f"Columns: {demo_small.columns.tolist()}")
print(f"Saved to: {OUTPUT}")