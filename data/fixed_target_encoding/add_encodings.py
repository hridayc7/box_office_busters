import pandas as pd

# Read the data from the CSV file into a DataFrame
df = pd.read_csv('sorted_data.csv')

# Calculate and add actor_0_name_encoded
df['actor_0_name_encoded'] = df['actor0_rev'] / \
    df['actor0_movies'].replace(0, 1)

# Calculate and add actor_1_name_encoded
df['actor_1_name_encoded'] = df['actor1_rev'] / \
    df['actor1_movies'].replace(0, 1)

# Calculate and add actor_2_name_encoded
df['actor_2_name_encoded'] = df['actor2_rev'] / \
    df['actor2_movies'].replace(0, 1)

# Output the modified DataFrame to a new CSV file
df.to_csv('almost_preprocessed.csv', index=False)
