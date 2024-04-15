import pandas as pd

# Load the dataset
data = pd.read_csv(
    "april_filtered_preprocessed.csv")

# Convert strings representing lists to actual lists
data['genres'] = data['genres'].apply(eval)

# Create a set to store all unique genre names
unique_genres = set()

# Iterate over each row and collect all unique genre names
for genres_list in data['genres']:
    unique_genres.update(genres_list)

# Create new columns for each unique genre and fill them with zeros
for genre in unique_genres:
    data[genre] = 0

# Iterate over each row and set the corresponding genre column to 1
for idx, row in data.iterrows():
    for genre in row['genres']:
        data.at[idx, genre] = 1

# Drop the original 'genres' column since it's no longer needed
data.drop('genres', axis=1, inplace=True)

# Output the expanded dataset to a new CSV file
data.to_csv("your_dataset_one_hot_encoded.csv", index=False)
