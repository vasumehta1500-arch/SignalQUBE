import pandas as pd
from load_data import FAERSLoader


class DataValidator:
    """
    Validate FAERS datasets before analysis.
    """

    def __init__(self):
        self.loader = FAERSLoader()

    def validate_dataset(self, name, df):

        print("\n" + "=" * 70)
        print(f"VALIDATING {name} DATASET")
        print("=" * 70)

        # Dataset Shape
        print(f"\nRows    : {df.shape[0]:,}")
        print(f"Columns : {df.shape[1]}")

        # Data Types
        print("\nData Types")
        print("-" * 50)
        print(df.dtypes)

        # Missing Values
        print("\nMissing Values")
        print("-" * 50)
        print(df.isnull().sum())

        # Duplicate Rows
        duplicates = df.duplicated().sum()

        print("\nDuplicate Rows")
        print("-" * 50)
        print(duplicates)

        # Duplicate Primary IDs
        if "primaryid" in df.columns:

            duplicate_ids = df["primaryid"].duplicated().sum()

            print("\nDuplicate Primary IDs")
            print("-" * 50)
            print(duplicate_ids)

        # Memory Usage
        memory = df.memory_usage(deep=True).sum() / (1024 ** 2)

        print("\nMemory Usage")
        print("-" * 50)
        print(f"{memory:.2f} MB")

        print("\nValidation Complete ✓")