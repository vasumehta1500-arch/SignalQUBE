# Import the FAERSLoader class
from load_data import FAERSLoader

# Create loader object
loader = FAERSLoader()

# Load all datasets
demo = loader.load_demo()
drug = loader.load_drug()
reac = loader.load_reac()
outc = loader.load_outc()

# Store datasets in a dictionary
datasets = {
    "DEMO": demo,
    "DRUG": drug,
    "REAC": reac,
    "OUTC": outc
}

# Loop through each dataset
for name, df in datasets.items():

    print("\n" + "=" * 60)
    print(f"{name} DATASET")
    print("=" * 60)

    # Display shape
    print("\nShape:")
    print(df.shape)

    # Display column names
    print("\nColumns:")
    print(df.columns.tolist())

    # Display first five rows
    print("\nFirst 5 Rows:")
    print(df.head())

    # Display missing values
    print("\nMissing Values:")
    print(df.isnull().sum())

    # Display duplicate rows
    print("\nDuplicate Rows:")
    print(df.duplicated().sum())