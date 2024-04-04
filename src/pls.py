import pandas as pd

# Assuming 'data' contains the provided dataset as a list of dictionaries
# Convert the list of dictionaries to a pandas DataFrame
data = pd.read_csv("../data/super_regression/movie_data.csv")
df = pd.DataFrame(data)

# Filter out rows where any of the actor names are None
df = df.dropna(subset=['actor_0_name', 'actor_1_name', 'actor_2_name'])

# Print the filtered DataFrame

# Assuming 'filtered_data.csv' as the desired filename for the CSV file
csv_filename = 'filtered_data.csv'

# Convert the filtered DataFrame back to a CSV file
df.to_csv(csv_filename, index=False)
print(f"Filtered data saved to {csv_filename}")