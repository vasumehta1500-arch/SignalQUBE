import pandas as pd
from pathlib import Path


INPUT_FILE = Path(
    "data/processed/2025Q4/signal_results.csv"
)

OUTPUT_FILE = Path(
    "src/ml/training_data.csv"
)


def main():

    print("=" * 60)
    print("SIGNALQUBE ML DATASET PREPARATION")
    print("=" * 60)

    # --------------------------------------------------
    # LOAD SIGNAL RESULTS
    # --------------------------------------------------

    print(f"\nLoading: {INPUT_FILE}")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Signal results not found: {INPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE)

    print(f"Original signal pairs: {len(df):,}")

    # --------------------------------------------------
    # REQUIRED FEATURES
    # --------------------------------------------------

    features = [
        "A",
        "B",
        "C",
        "D",
        "PRR",
        "ROR",
        "ChiSquare",
        "ROR_Lower95"
    ]

    missing = [
        column
        for column in features
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns: {missing}"
        )

    # --------------------------------------------------
    # SELECT ML FEATURES
    # --------------------------------------------------

    ml_df = df[features].copy()

    # Convert everything to numeric
    for column in features:
        ml_df[column] = pd.to_numeric(
            ml_df[column],
            errors="coerce"
        )

    # Remove invalid values
    ml_df = ml_df.replace(
        [float("inf"), float("-inf")],
        pd.NA
    )

    ml_df = ml_df.dropna()

    print(
        f"After cleaning: {len(ml_df):,}"
    )

    # --------------------------------------------------
    # REMOVE EXTREME VALUES
    # --------------------------------------------------

    ml_df = ml_df[
        (ml_df["PRR"] < 1000) &
        (ml_df["ROR"] < 100000)
    ].copy()

    print(
        f"After outlier filtering: "
        f"{len(ml_df):,}"
    )

    # --------------------------------------------------
    # CREATE ML LABEL
    # --------------------------------------------------

    # Statistically supported signal:
    #
    # PRR >= 2
    # Chi-square >= 4
    # ROR Lower 95% > 1
    #
    # All conditions must be satisfied.

    ml_df["Label"] = (
        (ml_df["PRR"] >= 2) &
        (ml_df["ChiSquare"] >= 4) &
        (ml_df["ROR_Lower95"] > 1)
    ).astype(int)

    # --------------------------------------------------
    # DISPLAY CLASS DISTRIBUTION
    # --------------------------------------------------

    print("\nClass Distribution")
    print("-" * 40)

    print(
        ml_df["Label"]
        .value_counts()
        .sort_index()
    )

    print("\nClass Percentage")
    print("-" * 40)

    print(
        (
            ml_df["Label"]
            .value_counts(normalize=True)
            .sort_index()
            * 100
        ).round(2)
    )

    # --------------------------------------------------
    # SAVE DATASET
    # --------------------------------------------------

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    ml_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\n" + "=" * 60)
    print("ML DATASET CREATED SUCCESSFULLY")
    print("=" * 60)

    print(f"\nRows    : {len(ml_df):,}")
    print(f"Columns : {ml_df.shape[1]}")

    print(f"\nSaved to:")
    print(OUTPUT_FILE)

    print("\nFirst 5 rows:")
    print(ml_df.head())


if __name__ == "__main__":
    main()