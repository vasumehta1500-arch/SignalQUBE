import pandas as pd
from pathlib import Path

class DataCleaner:

    def __init__(self):
        # Folder where cleaned datasets will be stored
        self.output_path = Path("data/processed")

        # Create folder if it doesn't exist
        self.output_path.mkdir(parents=True, exist_ok=True)

    def clean_column_names(self, df):
        """
        Convert column names to lowercase and remove spaces.
        """
        df.columns = (
            df.columns
            .str.lower()
            .str.strip()
            .str.replace(" ", "_")
        )
        return df

    def remove_duplicates(self, df):
        """
        Remove duplicate rows.
        """
        before = len(df)

        df = df.drop_duplicates()

        after = len(df)

        print(f"Duplicates Removed : {before - after}")

        return df

    def missing_values(self, df):
        """
        Display missing values.
        """
        print("\nMissing Values")
        print("-" * 40)

        print(df.isnull().sum())

    def dataset_info(self, df):
        """
        Display dataset information.
        """
        print("\nShape :", df.shape)
        print("\nColumns :")
        print(df.columns.tolist())

    def save_dataset(self, df, filename):
        """
        Save cleaned dataset.
        """

        file_path = self.output_path / filename

        df.to_csv(file_path, index=False)

        print(f"\nSaved : {file_path}")
    