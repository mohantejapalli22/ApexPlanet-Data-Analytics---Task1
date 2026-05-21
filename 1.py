import pandas as pd
import os
from dateutil import parser

print("Looking in:", os.getcwd())

# Build the correct path to the dataset
base_dir = os.path.dirname(os.path.dirname(__file__))   # go up from python_files to data analytics
csv_path = os.path.join(base_dir, "datasets", "transactions_raw.csv")

# Read the raw dataset
df = pd.read_csv(csv_path)

# Remove duplicates
df = df.drop_duplicates()

# Standardize date formats
df['TransactionDate'] = df['TransactionDate'].apply(
    lambda x: parser.parse(str(x), dayfirst=False) if pd.notnull(x) else pd.NaT
)
df['DateOfBirth'] = pd.to_datetime(df['DateOfBirth'], errors='coerce')

# Handle missing values
df['Amount'] = df['Amount'].fillna(0)

# Remove invalid negative amounts
df = df[df['Amount'] >= 0]

# Normalize product categories
df['ProductCategory'] = df['ProductCategory'].str.lower().str.strip()

# Feature engineering: Customer Age
df['CustomerAge'] = (pd.Timestamp.today() - df['DateOfBirth']).dt.days // 365

# Print cleaned dataset
print(df)

# Save cleaned dataset back into datasets folder
output_path = os.path.join(base_dir, "datasets", "transactions_cleaned.csv")
df.to_csv(output_path, index=False)
print("Cleaned dataset saved as transactions_cleaned.csv")
