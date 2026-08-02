import pandas as pd
from pathlib import Path


class FAERSLoader:
    # Class to load FAERS datasets

    def __init__(self):
        # Path to the raw data folder
        self.raw_data = Path("data/raw")

    def load_file(self, filename):
        """
        Generic function to load a FAERS file.

        Parameters:
            filename (str): Name of the file

        Returns:
            pandas.DataFrame
        """

        # Create complete file path
        file_path = self.raw_data / filename

        # Display the file currently being loaded
        print(f"\nLoading {filename}...")

        # Read the dataset
        df = pd.read_csv(
            file_path,
            sep="$",
            encoding="latin1",
            low_memory=False
        )

        # Display dataset dimensions
        print(f"Rows    : {df.shape[0]:,}")
        print(f"Columns : {df.shape[1]}")

        return df

    def load_demo(self):
        """Load DEMO dataset."""
        return self.load_file("DEMO25Q4.txt")

    def load_drug(self):
        """Load DRUG dataset."""
        return self.load_file("DRUG25Q4.txt")

    def load_reac(self):
        """Load REAC dataset."""
        return self.load_file("REAC25Q4.txt")

    def load_outc(self):
        """Load OUTC dataset."""
        return self.load_file("OUTC25Q4.txt")


