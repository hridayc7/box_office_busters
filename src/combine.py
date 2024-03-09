import pandas as pd
import ast

def string_to_list(column_data):
    try:
        # Convert the string representation of list/dict to actual list/dict
        data = ast.literal_eval(column_data)
        if isinstance(data, list):  # Check if data is a list
            # Extract names from each dictionary in the list
            return [item['name'] for item in data if 'name' in item]
        return []  # Return an empty list if data is not a list
    except (ValueError, SyntaxError):  # In case of evaluation error or if data is NaN
        return []  # Return an empty list

# List of your CSV files
csv_files = ['../data/tmdb/tmdb_info_1.csv', '../data/tmdb/tmdb_info_2.csv', '../data/tmdb/tmdb_info_3.csv', '../data/tmdb/tmdb_info_4.csv', '../data/tmdb/tmdb_info_5.csv']

dfs = []  # List to store each individual DataFrame
chunk_size = 500  # You can adjust this size

for file in csv_files:
    chunks = []
    for chunk in pd.read_csv(file, chunksize=chunk_size, on_bad_lines='skip'):
        chunks.append(chunk)
    df = pd.concat(chunks, ignore_index=True)
    dfs.append(df)

# Combine all DataFrames from each file into one large DataFrame
combined_df = pd.concat(dfs, ignore_index=True)

combined_df = combined_df.drop_duplicates()

# Convert 'budget' to numeric, drop NaNs, and filter out zero budgets
combined_df['budget'] = pd.to_numeric(combined_df['budget'], errors='coerce')
combined_df = combined_df.dropna(subset=['budget'])
combined_df = combined_df[combined_df['budget'] != 0]

combined_df['revenue'] = pd.to_numeric(combined_df['revenue'], errors='coerce')
combined_df = combined_df.dropna(subset=['revenue'])
combined_df = combined_df[combined_df['revenue'] != 0]

columns_to_drop = ['backdrop_path', 'belongs_to_collection', 'homepage', 'poster_path', 'video',
                   'belongs_to_collection.id', 'belongs_to_collection.name', 
                   'belongs_to_collection.poster_path', 'belongs_to_collection.backdrop_path']
combined_df = combined_df.drop(columns=columns_to_drop, errors='ignore')

combined_df['genres'] = combined_df['genres'].apply(string_to_list)
combined_df['production_companies'] = combined_df['production_companies'].apply(string_to_list)
combined_df['production_countries'] = combined_df['production_countries'].apply(string_to_list)
combined_df['spoken_languages'] = combined_df['spoken_languages'].apply(string_to_list)

# Save the processed DataFrame
combined_df.to_csv('../data/tmdb/combined_tmdb_data.csv', index=False)
