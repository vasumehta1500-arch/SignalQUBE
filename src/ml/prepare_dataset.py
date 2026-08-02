import sys
from pathlib import Path
import pandas as pd

# Add project root
sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.analysis.signal_detection import SignalDetector


def main():

    detector = SignalDetector()

    print("Loading FAERS data...")
    merged = detector.prepare_data()

    print(f"Total merged records: {len(merged):,}")

    pairs = detector.top_drug_reaction_pairs(400)

    dataset = []

    for index, (_, row) in enumerate(pairs.iterrows(), start=1):

        print(f"Processing {index}/{len(pairs)}", end="\r")

        result = detector.calculate_signal(
            row["drugname"],
            row["pt"]
        )

        if result is None:
            continue

        if result["PRR"] is None:
            continue

        dataset.append({
            "A": result["A"],
            "B": result["B"],
            "C": result["C"],
            "D": result["D"],
            "PRR": result["PRR"],
            "ROR": result["ROR"],
            "Label": 1 if result["PRR"] >= 2 else 0
        })

    df = pd.DataFrame(dataset)

    output = Path(__file__).parent / "training_data.csv"

    df.to_csv(output, index=False)

    print("\n")
    print("=" * 50)
    print("Dataset Created Successfully")
    print(df.head())
    print("=" * 50)


if __name__ == "__main__":
    main()