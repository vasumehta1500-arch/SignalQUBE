import pandas as pd
import numpy as np

print("===================================")
print("FAERS Signal Detection Project")
print("Project setup successful!")
print("===================================")

from load_data import FAERSLoader
from preprocess import DataCleaner

# Create objects
loader = FAERSLoader()
cleaner = DataCleaner()

# Load datasets
datasets = {
    "demo_clean.csv": loader.load_demo(),
    "drug_clean.csv": loader.load_drug(),
    "reac_clean.csv": loader.load_reac(),
    "outc_clean.csv": loader.load_outc()
}

# Clean every dataset
for filename, df in datasets.items():

    print("\n" + "=" * 60)
    print(filename)
    print("=" * 60)

    df = cleaner.clean_column_names(df)
    df = cleaner.remove_duplicates(df)

    cleaner.dataset_info(df)
    cleaner.missing_values(df)

    cleaner.save_dataset(df, filename)