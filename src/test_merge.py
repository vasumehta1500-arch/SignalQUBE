from merge_data import DataMerger


merger = DataMerger()


demo, drug, reac, outc = merger.load_processed_data()

# Merge DEMO + DRUG
merged_df = merger.merge_demo_drug(demo, drug)

# Merge REAC
merged_df = merger.merge_reac(merged_df, reac)

# Merge OUTC
merged_df = merger.merge_outc(merged_df, outc)

# Save final dataset
merger.save_master_dataset(merged_df)

print("\n")
print("=" * 60)
print("MASTER DATASET PREVIEW")
print("=" * 60)

print(merged_df.head())

print("\n")

print("Number of Rows :", len(merged_df))
print("Number of Columns :", len(merged_df.columns))
print("Unique Patients :", merged_df["primaryid"].nunique())