import pandas as pd

# Assuming your dataset is stored in a CSV file named 'movie_data.csv'
file_path = 'Final_Regression.csv'

# Read the dataset into a DataFrame
df = pd.read_csv(file_path)

# List of columns to drop containing the word "encodings"
columns_to_drop = [col for col in df.columns if 'encoded' in col]

# Drop the columns
df.drop(columns=columns_to_drop, inplace=True)

# Save the modified DataFrame back to a CSV file
df.to_csv('cleaned_movie_data.csv', index=False)
