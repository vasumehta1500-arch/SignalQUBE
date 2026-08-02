from load_data import FAERSLoader
from validate_data import DataValidator

loader = FAERSLoader()
validator = DataValidator()

# Load datasets
demo = loader.load_demo()
drug = loader.load_drug()
reac = loader.load_reac()
outc = loader.load_outc()

# Validate each dataset
validator.validate_dataset("DEMO", demo)
validator.validate_dataset("DRUG", drug)
validator.validate_dataset("REAC", reac)
validator.validate_dataset("OUTC", outc)