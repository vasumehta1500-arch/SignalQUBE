import pandas as pd
from pathlib import Path


class DataMerger:
    """
    Class for loading and merging cleaned FAERS datasets.
    """

    def __init__(self, year="2025", quarter="Q4"):

        self.year = str(year)
        self.quarter = quarter.upper()

        # Quarter-specific processed data
        self.processed_path = (
            Path("data/processed")
            / f"{self.year}{self.quarter}"
        )

        self.processed_path.mkdir(
            parents=True,
            exist_ok=True
        )

    def load_processed_data(self):
        """
        Load all cleaned datasets.
        """

        print("\nLoading cleaned datasets...\n")

        demo = pd.read_csv(
            self.processed_path / "demo_clean.csv",
            low_memory=False
        )

        drug = pd.read_csv(
            self.processed_path / "drug_clean.csv",
            low_memory=False
        )

        reac = pd.read_csv(
            self.processed_path / "reac_clean.csv",
            low_memory=False
        )

        outc = pd.read_csv(
            self.processed_path / "outc_clean.csv",
            low_memory=False
        )

        print(f"DEMO : {demo.shape}")
        print(f"DRUG : {drug.shape}")
        print(f"REAC : {reac.shape}")
        print(f"OUTC : {outc.shape}")

        return demo, drug, reac, outc

    def merge_demo_drug(self, demo, drug):

        print("\n" + "=" * 60)
        print("MERGING DEMO + DRUG")
        print("=" * 60)

        merged_df = pd.merge(
            demo,
            drug,
            on="primaryid",
            how="left"
        )

        print(f"DEMO Shape   : {demo.shape}")
        print(f"DRUG Shape   : {drug.shape}")
        print(f"Merged Shape : {merged_df.shape}")

        return merged_df

    def merge_reac(self, merged_df, reac):

        print("\n" + "=" * 60)
        print("MERGING REAC")
        print("=" * 60)

        merged_df = pd.merge(
            merged_df,
            reac,
            on="primaryid",
            how="left"
        )

        print(
            f"Shape After REAC Merge : "
            f"{merged_df.shape}"
        )

        return merged_df

    def merge_outc(self, merged_df, outc):

        print("\n" + "=" * 60)
        print("MERGING OUTC")
        print("=" * 60)

        merged_df = pd.merge(
            merged_df,
            outc,
            on="primaryid",
            how="left"
        )

        print(
            f"Final Shape : {merged_df.shape}"
        )

        return merged_df

    def save_master_dataset(self, merged_df):

        output_file = (
            self.processed_path
            / "master_dataset.csv"
        )

        merged_df.to_csv(
            output_file,
            index=False
        )

        print(
            "\nMaster dataset saved successfully!"
        )

        print(
            f"Location : {output_file}"
        )