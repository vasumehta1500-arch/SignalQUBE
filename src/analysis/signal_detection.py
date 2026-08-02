import pandas as pd


class SignalDetector:

    def __init__(self):
        self.processed_path = "data/processed/"
        self._merged = None

    def load_data(self):

        drug = pd.read_csv(
            self.processed_path + "drug_clean.csv",
            low_memory=False
        )

        reac = pd.read_csv(
            self.processed_path + "reac_clean.csv",
            low_memory=False
        )

        return drug, reac

    def prepare_data(self):

        if self._merged is not None:
            return self._merged

        drug, reac = self.load_data()

        drug["drugname"] = (
            drug["drugname"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        reac["pt"] = (
            reac["pt"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        suspect_drugs = drug[
            drug["role_cod"].isin(["PS", "SS"])
        ]

        self._merged = pd.merge(
            suspect_drugs,
            reac,
            on="primaryid",
            how="inner"
        )

        return self._merged

    def top_drug_reaction_pairs(self, top_n=20):

        merged = self.prepare_data()

        result = (
            merged.groupby(["drugname", "pt"])
            .size()
            .reset_index(name="Reports")
            .sort_values(
                by="Reports",
                ascending=False
            )
            .head(top_n)
        )

        return result

    def calculate_signal(self, drug_name, reaction_name):

        merged = self.prepare_data()

        drug_name = drug_name.strip().upper()
        reaction_name = reaction_name.strip().upper()

        A = len(
            merged[
                (merged["drugname"] == drug_name) &
                (merged["pt"] == reaction_name)
            ]
        )

        B = len(
            merged[
                (merged["drugname"] == drug_name) &
                (merged["pt"] != reaction_name)
            ]
        )

        C = len(
            merged[
                (merged["drugname"] != drug_name) &
                (merged["pt"] == reaction_name)
            ]
        )

        D = len(
            merged[
                (merged["drugname"] != drug_name) &
                (merged["pt"] != reaction_name)
            ]
        )

        print("=" * 50)
        print("Drug:", drug_name)
        print("Reaction:", reaction_name)
        print(f"A={A}, B={B}, C={C}, D={D}")
        print("=" * 50)

        # No signal found
        if A == 0:
            return {
                "Drug": drug_name,
                "Reaction": reaction_name,
                "A": A,
                "B": B,
                "C": C,
                "D": D,
                "PRR": None,
                "ROR": None,
                "Signal": "⚪ No Signal"
            }

        # Haldane correction
        A_adj = A if A > 0 else 0.5
        B_adj = B if B > 0 else 0.5
        C_adj = C if C > 0 else 0.5
        D_adj = D if D > 0 else 0.5

        prr = (
            (A_adj / (A_adj + B_adj))
            /
            (C_adj / (C_adj + D_adj))
        )

        ror = (
            (A_adj * D_adj)
            /
            (B_adj * C_adj)
        )

        if prr >= 5:
            signal = "🔴 Strong"
        elif prr >= 2:
            signal = "🟡 Moderate"
        else:
            signal = "🟢 Weak"

        return {
            "Drug": drug_name,
            "Reaction": reaction_name,
            "A": A,
            "B": B,
            "C": C,
            "D": D,
            "PRR": round(prr, 3),
            "ROR": round(ror, 3),
            "Signal": signal
        }

    def clear_cache(self):
        self._merged = None