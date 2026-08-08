from pathlib import Path
import pandas as pd

from preprocess import DataCleaner


def process_file(
    input_path,
    output_path,
    cleaner
):
    """
    Load, clean and save one FAERS dataset.
    """

    print("\n" + "=" * 60)
    print(f"Processing: {input_path.name}")
    print("=" * 60)

    # Load FDA dataset
    df = pd.read_csv(
        input_path,
        sep="$",
        encoding="latin1",
        low_memory=False
    )

    print(
        f"Original Shape : {df.shape}"
    )

    # Clean column names
    df = cleaner.clean_column_names(df)

    # Remove duplicate rows
    df = cleaner.remove_duplicates(df)

    # Show missing values
    cleaner.missing_values(df)

    # Show final information
    cleaner.dataset_info(df)

    # Save cleaned dataset
    cleaner.save_dataset(
        df,
        output_path
    )


def main():

    # --------------------------------------------------
    # FDA QUARTER
    # --------------------------------------------------

    year = "2025"
    quarter = "Q4"

    # --------------------------------------------------
    # INPUT / OUTPUT PATHS
    # --------------------------------------------------

    input_path = (
        Path("data/raw")
        / f"{year}{quarter}"
        / "ASCII"
    )

    cleaner = DataCleaner(
        year=year,
        quarter=quarter
    )

    print("=" * 60)
    print("SIGNALQUBE FDA PREPROCESSING")
    print("=" * 60)

    print(
        f"Input : {input_path}"
    )

    print(
        f"Output: {cleaner.output_path}"
    )

    # --------------------------------------------------
    # FILES REQUIRED FOR CURRENT ANALYSIS
    # --------------------------------------------------

    files = {
        "DEMO": (
            "DEMO25Q4.txt",
            "demo_clean.csv"
        ),
        "DRUG": (
            "DRUG25Q4.txt",
            "drug_clean.csv"
        ),
        "REAC": (
            "REAC25Q4.txt",
            "reac_clean.csv"
        ),
        "OUTC": (
            "OUTC25Q4.txt",
            "outc_clean.csv"
        )
    }

    # --------------------------------------------------
    # PROCESS EACH DATASET
    # --------------------------------------------------

    for dataset_name, (
        input_file,
        output_file
    ) in files.items():

        source = (
            input_path / input_file
        )

        if not source.exists():

            raise FileNotFoundError(
                f"\n{dataset_name} file not found:\n"
                f"{source}"
            )

        process_file(
            source,
            output_file,
            cleaner
        )

    print("\n" + "=" * 60)
    print("PREPROCESSING COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()