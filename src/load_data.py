import pandas as pd
from pathlib import Path


class FAERSLoader:
    """
    Loads FDA FAERS quarterly datasets.
    """

    def __init__(self, year="2025", quarter="Q4"):
        self.raw_data = (
            Path("data/raw")
            / f"{year}{quarter}"
            / "ASCII"
        )

    def load_file(self, filename):
        """
        Generic function to load a FAERS file.
        """

        file_path = self.raw_data / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"FAERS file not found:\n{file_path}"
            )

        print(f"\nLoading {filename}...")

        df = pd.read_csv(
            file_path,
            sep="$",
            encoding="latin1",
            low_memory=False
        )

        print(f"Rows    : {df.shape[0]:,}")
        print(f"Columns : {df.shape[1]}")

        return df

    def load_demo(self):
        return self.load_file("DEMO25Q4.txt")

    def load_drug(self):
        return self.load_file("DRUG25Q4.txt")

    def load_reac(self):
        return self.load_file("REAC25Q4.txt")

    def load_outc(self):
        return self.load_file("OUTC25Q4.txt")

    def load_indi(self):
        return self.load_file("INDI25Q4.txt")

    def load_ther(self):
        return self.load_file("THER25Q4.txt")

    def load_rpsr(self):
        return self.load_file("RPSR25Q4.txt")
