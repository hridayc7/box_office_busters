import pandas as pd

# Read the CSV files
april_df = pd.read_csv("april.csv")
combined_df = pd.read_csv("../data/tmdb/combined_tmdb_data.csv")

# Get the set of tmdb_ids present in the combined_df
combined_tmdb_ids = set(combined_df['id'])

# Filter April.csv to keep only the rows with tmdb_ids present in combined_tmdb_ids
april_df_filtered = april_df[april_df['tmdb_id'].isin(combined_tmdb_ids)]

# Write the filtered April.csv to a new CSV file
april_df_filtered.to_csv("filtered_April.csv", index=False)

print("Filtered April.csv has been saved successfully.")
