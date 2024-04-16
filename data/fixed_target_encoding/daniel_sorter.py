import pandas as pd

# Read the data from the CSV file into a DataFrame
df = pd.read_csv("sorted_data.csv")

# Sort the DataFrame by release year and release month
df_sorted = df.sort_values(by=["release_year", "release_month"])

# Output the sorted DataFrame to a CSV file
df_sorted.to_csv("sorted_data.csv", index=False)
