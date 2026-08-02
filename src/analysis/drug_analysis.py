import pandas as pd
from pathlib import Path
import plotly.express as px


class DrugAnalysis:

    def __init__(self):
        self.processed_path = Path("data/processed")
        self.result_path = Path("data/results")

        # Create results folder if it doesn't exist
        self.result_path.mkdir(parents=True, exist_ok=True)

    def load_data(self):

        file_path = self.processed_path / "drug_clean.csv"

        print("Loading Drug Dataset...\n")

        df = pd.read_csv(
            file_path,
            low_memory=False
        )

        return df

    def top_drugs(self, df, top_n=20):

        df = df.dropna(subset=["drugname"])

        df["drugname"] = df["drugname"].str.strip().str.upper()

        top = (
            df["drugname"]
            .value_counts()
            .head(top_n)
            .reset_index()
        )

        top.columns = ["Drug", "Reports"]

        return top

    def create_chart(self, top):

        fig = px.bar(
            top,
            x="Reports",
            y="Drug",
            orientation="h",
            title="Top 20 Reported Drugs in FAERS",
            text="Reports"
        )

        fig.update_layout(
            yaxis=dict(categoryorder="total ascending"),
            height=700
        )

        fig.write_html(
            self.result_path / "top20_drugs.html"
        )

        

        print("\nChart saved successfully!")