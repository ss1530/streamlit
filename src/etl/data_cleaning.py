import pandas as pd
import os

# Load the Excel dataset
data = pd.read_excel("./data/raw/savsnet_data.xlsx")
output_dir = "./data/cleaned"

# Data Cleaning

## 0. Handle Missing Values
data.fillna("Unknown", inplace=True)

## 1. Convert Consult_date to Datetime
data["Consult_date"] = pd.to_datetime(data["Consult_date"])

## 2. Standardize Species Names (make lowercase)
data["Species"] = data["Species"].str.lower()

# Splitting into DataFrames
df_cats = data[data["Species"] == "cat"]
df_dogs = data[data["Species"] == "dog"]
df_other = data[~data["Species"].isin(["cat", "dog"])]  # Catch-all for other species

# Optional: Save the Cleaned DataFrames
df_cats.to_csv(os.path.join(output_dir, "cats_consultations.csv"), index=False)
df_dogs.to_csv(os.path.join(output_dir, "dogs_consultations.csv"), index=False)
df_other.to_csv(
    os.path.join(output_dir, "other_species_consultations.csv"), index=False
)

# Print a Summary for Verification
print("Cats:")
print(df_cats.head())
print("Dogs:")
print(df_dogs.head())
print("Other Species:")
print(df_other.head())
