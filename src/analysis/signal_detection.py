import pandas as pd
import numpy as np
from pathlib import Path


class SignalDetector:

    def __init__(self, data_path="data/sample"):
        self.processed_path = Path(data_path)
        self._pairs = None
        self._signal_table = None

    # --------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------

    def load_data(self):

        drug_file = self.processed_path / "drug_clean.csv"
        reac_file = self.processed_path / "reac_clean.csv"

        if not drug_file.exists():
            raise FileNotFoundError(
                f"Drug dataset not found: {drug_file}"
            )

        if not reac_file.exists():
            raise FileNotFoundError(
                f"Reaction dataset not found: {reac_file}"
            )

        print("Loading DRUG...")

        drug = pd.read_csv(
            drug_file,
            usecols=[
                "primaryid",
                "drugname",
                "role_cod"
            ],
            low_memory=False
        )

        print("Loading REAC...")

        reac = pd.read_csv(
            reac_file,
            usecols=[
                "primaryid",
                "pt"
            ],
            low_memory=False
        )

        return drug, reac

    # --------------------------------------------------
    # CREATE UNIQUE REPORT RELATIONSHIPS
    # --------------------------------------------------

    def prepare_data(self):

        if self._pairs is not None:
            return self._pairs

        drug, reac = self.load_data()

        # Clean drug names
        drug["drugname"] = (
            drug["drugname"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        # Clean reaction names
        reac["pt"] = (
            reac["pt"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        # --------------------------------------------------
        # KEEP SUSPECT DRUGS
        # --------------------------------------------------

        drug = drug[
            drug["role_cod"].isin(["PS", "SS"])
        ].copy()

        # Unique report-drug relationships
        drug = (
            drug[
                ["primaryid", "drugname"]
            ]
            .drop_duplicates()
        )

        # Unique report-reaction relationships
        reac = (
            reac[
                ["primaryid", "pt"]
            ]
            .drop_duplicates()
        )

        print(
            f"Unique report-drug relationships: "
            f"{len(drug):,}"
        )

        print(
            f"Unique report-reaction relationships: "
            f"{len(reac):,}"
        )

        # --------------------------------------------------
        # CREATE DRUG-REACTION RELATIONSHIPS
        # --------------------------------------------------

        pairs = pd.merge(
            drug,
            reac,
            on="primaryid",
            how="inner"
        )

        # Remove duplicate report/drug/reaction combinations
        pairs = pairs.drop_duplicates(
            subset=[
                "primaryid",
                "drugname",
                "pt"
            ]
        )

        print(
            f"Unique report-drug-reaction relationships: "
            f"{len(pairs):,}"
        )

        self._pairs = pairs

        return pairs

    # --------------------------------------------------
    # BUILD REPORT-LEVEL SIGNAL TABLE
    # --------------------------------------------------

    def build_signal_table(self, min_count=3):

        if self._signal_table is not None:
            return self._signal_table

        pairs = self.prepare_data()

        # Number of unique reports
        total_reports = pairs[
            "primaryid"
        ].nunique()

        print(
            f"\nTotal unique reports: "
            f"{total_reports:,}"
        )

        # --------------------------------------------------
        # A = Drug AND Reaction
        # --------------------------------------------------

        A = (
            pairs
            .groupby(
                ["drugname", "pt"]
            )["primaryid"]
            .nunique()
            .reset_index(
                name="A"
            )
        )

        # --------------------------------------------------
        # Total reports containing each drug
        # --------------------------------------------------

        drug_counts = (
            pairs
            .groupby(
                "drugname"
            )["primaryid"]
            .nunique()
            .reset_index(
                name="drug_reports"
            )
        )

        # --------------------------------------------------
        # Total reports containing each reaction
        # --------------------------------------------------

        reaction_counts = (
            pairs
            .groupby(
                "pt"
            )["primaryid"]
            .nunique()
            .reset_index(
                name="reaction_reports"
            )
        )

        # --------------------------------------------------
        # MERGE COUNTS
        # --------------------------------------------------

        result = A.merge(
            drug_counts,
            on="drugname",
            how="left"
        )

        result = result.merge(
            reaction_counts,
            on="pt",
            how="left"
        )

        # --------------------------------------------------
        # MINIMUM COUNT FILTER
        # --------------------------------------------------

        result = result[
            result["A"] >= min_count
        ].copy()

        # --------------------------------------------------
        # B = Drug present, Reaction absent
        # --------------------------------------------------

        result["B"] = (
            result["drug_reports"]
            - result["A"]
        )

        # --------------------------------------------------
        # C = Reaction present, Drug absent
        # --------------------------------------------------

        result["C"] = (
            result["reaction_reports"]
            - result["A"]
        )

        # --------------------------------------------------
        # D = Neither Drug nor Reaction
        # --------------------------------------------------

        result["D"] = (
            total_reports
            - result["A"]
            - result["B"]
            - result["C"]
        )

        # Protect against numerical issues
        result["B"] = result["B"].clip(lower=0)
        result["C"] = result["C"].clip(lower=0)
        result["D"] = result["D"].clip(lower=0)

        # --------------------------------------------------
        # HALDANE CORRECTION
        # --------------------------------------------------

        result["A_adj"] = result["A"].clip(lower=0.5)
        result["B_adj"] = result["B"].clip(lower=0.5)
        result["C_adj"] = result["C"].clip(lower=0.5)
        result["D_adj"] = result["D"].clip(lower=0.5)

        # --------------------------------------------------
        # PRR
        # --------------------------------------------------

        result["PRR"] = (
            (
                result["A_adj"]
                /
                (
                    result["A_adj"]
                    +
                    result["B_adj"]
                )
            )
            /
            (
                result["C_adj"]
                /
                (
                    result["C_adj"]
                    +
                    result["D_adj"]
                )
            )
        )

        # --------------------------------------------------
        # ROR
        # --------------------------------------------------

        result["ROR"] = (
            (
                result["A_adj"]
                *
                result["D_adj"]
            )
            /
            (
                result["B_adj"]
                *
                result["C_adj"]
            )
        )

        # --------------------------------------------------
        # CHI-SQUARE
        # --------------------------------------------------

        numerator = (
            total_reports
            *
            (
                result["A"] * result["D"]
                -
                result["B"] * result["C"]
            ) ** 2
        )

        denominator = (
            (result["A"] + result["B"])
            *
            (result["C"] + result["D"])
            *
            (result["A"] + result["C"])
            *
            (result["B"] + result["D"])
        )

        result["ChiSquare"] = (
            numerator / denominator.replace(
                0,
                np.nan
            )
        )

        result["ChiSquare"] = (
            result["ChiSquare"]
            .replace(
                [np.inf, -np.inf],
                np.nan
            )
            .fillna(0)
        )

        # --------------------------------------------------
        # ROR 95% CONFIDENCE INTERVAL
        # --------------------------------------------------

        log_ror_se = np.sqrt(
            (1 / result["A_adj"])
            +
            (1 / result["B_adj"])
            +
            (1 / result["C_adj"])
            +
            (1 / result["D_adj"])
        )

        result["ROR_Lower95"] = np.exp(
            np.log(result["ROR"])
            -
            1.96 * log_ror_se
        )

        result["ROR_Upper95"] = np.exp(
            np.log(result["ROR"])
            +
            1.96 * log_ror_se
        )

        # --------------------------------------------------
        # SIGNAL CLASSIFICATION
        # --------------------------------------------------

        result["Signal"] = "🟢 Weak"

        # Moderate signal
        moderate = (
            (result["A"] >= min_count)
            &
            (result["PRR"] >= 2)
            &
            (result["ChiSquare"] >= 4)
        )

        result.loc[
            moderate,
            "Signal"
        ] = "🟡 Moderate"

        # Strong signal
        strong = (
            (result["A"] >= min_count)
            &
            (result["PRR"] >= 2)
            &
            (result["ChiSquare"] >= 4)
            &
            (result["ROR_Lower95"] > 1)
        )

        result.loc[
            strong,
            "Signal"
        ] = "🔴 Strong"

        # --------------------------------------------------
        # SORT RESULTS
        # --------------------------------------------------

        result = (
            result
            .sort_values(
                ["PRR", "A"],
                ascending=[
                    False,
                    False
                ]
            )
            .reset_index(
                drop=True
            )
        )

        self._signal_table = result

        print(
            f"\nFinal signal pairs: "
            f"{len(result):,}"
        )

        print("\nSignal distribution:")
        print(
            result["Signal"]
            .value_counts()
        )

        return result

    # --------------------------------------------------
    # TOP SIGNALS
    # --------------------------------------------------

    def top_signals(self, top_n=20):

        table = self.build_signal_table()

        return table[
            [
                "drugname",
                "pt",
                "A",
                "B",
                "C",
                "D",
                "PRR",
                "ROR",
                "ChiSquare",
                "ROR_Lower95",
                "ROR_Upper95",
                "Signal"
            ]
        ].head(top_n)

    # --------------------------------------------------
    # INDIVIDUAL SIGNAL
    # --------------------------------------------------

    def calculate_signal(
        self,
        drug_name,
        reaction_name
    ):

        table = self.build_signal_table(
            min_count=1
        )

        drug_name = (
            drug_name
            .strip()
            .upper()
        )

        reaction_name = (
            reaction_name
            .strip()
            .upper()
        )

        row = table[
            (table["drugname"] == drug_name)
            &
            (table["pt"] == reaction_name)
        ]

        if row.empty:

            return {
                "Drug": drug_name,
                "Reaction": reaction_name,
                "A": 0,
                "B": None,
                "C": None,
                "D": None,
                "PRR": None,
                "ROR": None,
                "ChiSquare": None,
                "ROR_Lower95": None,
                "ROR_Upper95": None,
                "Signal": "⚪ No Signal"
            }

        row = row.iloc[0]

        return {
            "Drug": drug_name,
            "Reaction": reaction_name,
            "A": int(row["A"]),
            "B": int(row["B"]),
            "C": int(row["C"]),
            "D": int(row["D"]),
            "PRR": round(
                float(row["PRR"]),
                3
            ),
            "ROR": round(
                float(row["ROR"]),
                3
            ),
            "ChiSquare": round(
                float(row["ChiSquare"]),
                3
            ),
            "ROR_Lower95": round(
                float(row["ROR_Lower95"]),
                3
            ),
            "ROR_Upper95": round(
                float(row["ROR_Upper95"]),
                3
            ),
            "Signal": row["Signal"]
        }

    # --------------------------------------------------
    # SAVE SIGNAL TABLE
    # --------------------------------------------------

    def save_signal_table(
        self,
        filename="signal_results.csv"
    ):

        table = self.build_signal_table()

        output_file = (
            self.processed_path
            / filename
        )

        table.to_csv(
            output_file,
            index=False
        )

        print(
            f"\nSaved signal table:"
            f"\n{output_file}"
        )

    # --------------------------------------------------
    # CLEAR CACHE
    # --------------------------------------------------

    def clear_cache(self):

        self._pairs = None
        self._signal_table = None