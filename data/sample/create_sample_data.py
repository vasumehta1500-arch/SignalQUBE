import os
import pandas as pd

SOURCE = "data/processed"
DEST = "data/sample"

os.makedirs(DEST, exist_ok=True)

files = [
    "demo_clean.csv",
    "drug_clean.csv",
    "reac_clean.csv",
    "outc_clean.csv"
]

for file in files:
    print(f"Processing {file}...")
    df = pd.read_csv(f"{SOURCE}/{file}", low_memory=False)

    # Take first 5000 rows
    df = df.head(5000)

    df.to_csv(f"{DEST}/{file}", index=False)

print("Sample dataset created successfully!")