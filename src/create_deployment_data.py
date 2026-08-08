import pandas as pd
from pathlib import Path


SOURCE = Path("data/processed/2025Q4/signal_results.csv")
OUTPUT = Path("data/deployment/signal_results.csv")


def main():

    print("Loading full signal results...")

    df = pd.read_csv(
        SOURCE,
        low_memory=False
    )

    print(f"Full signal pairs: {len(df):,}")

    # Keep meaningful signals
    deployment = df[
        (df["A"] >= 3)
    ].copy()

    # Sort strongest signals first
    deployment = deployment.sort_values(
        ["PRR", "A"],
        ascending=[False, False]
    )

    # Keep top 20,000 signals for dashboard
    deployment = deployment.head(20000)

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    deployment.to_csv(
        OUTPUT,
        index=False
    )

    print(
        f"Deployment records: {len(deployment):,}"
    )

    print(
        f"Saved to: {OUTPUT}"
    )


if __name__ == "__main__":
    main()