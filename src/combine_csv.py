import os
import pandas as pd

# List all CSV files in the directory
csv_files = [file for file in os.listdir() if file.startswith('output') and file.endswith('.csv')]

# Initialize an empty DataFrame to store the combined data
combined_df = pd.DataFrame()

# Iterate through each CSV file and concatenate its data to the combined DataFrame
for file in csv_files:
    df = pd.read_csv(file)
    combined_df = pd.concat([combined_df, df], ignore_index=True)

# Write the combined DataFrame to a new CSV file
combined_df.to_csv('combined_output.csv', index=False)
