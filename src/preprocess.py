import pandas as pd
import ast
import re
from sklearn.preprocessing import MultiLabelBinarizer, LabelBinarizer

def print_unique(column:str):
    #print(df[column].head(10))

    # Convert string representations of lists to actual lists
    df[column] = df[column].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

    # Extract all unique genres
    unique_values = set(genre for sublist in df[column] for genre in sublist)

    # Print the unique genres
    print(f'Unique values in {column} column: {unique_values}')

def one_hot_encode_list(column:str, df:pd.DataFrame) -> pd.DataFrame: 
    # Convert string representations of lists to actual lists
    df[column] = df[column].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    # Replace NaN with empty lists, and ensure all entries are lists
    df[column] = df[column].fillna('[]').apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

    # Initialize MultiLabelBinarizer
    mlb = MultiLabelBinarizer()

    # Fit and transform the column to one-hot encoded array
    column_encoded = mlb.fit_transform(df[column])

    # Create a DataFrame from the encoded array with names as column names
    column_encoded_df = pd.DataFrame(column_encoded, columns=mlb.classes_).astype(int)  # Convert to int here

    column_encoded_df = pd.DataFrame(column_encoded, columns=mlb.classes_, index=df.index).astype(int)  # Note the index=df.index part

    # Concatenate the original DataFrame with the new encoded DataFrame
    df = pd.concat([df, column_encoded_df], axis=1)

    # Optionally, drop the original column if you no longer need it
    df = df.drop(column, axis=1) 
    return df

def one_hot_encode_single(column: str, df: pd.DataFrame) -> pd.DataFrame:
    # Initialize LabelBinarizer
    lb = LabelBinarizer()
    
    # Fit and transform the column to one-hot encoded array
    # No need to convert column contents since they're already single string values
    column_encoded = lb.fit_transform(df[column])
    
    # Create a DataFrame from the encoded array with names as column names
    column_encoded_df = pd.DataFrame(column_encoded, columns=lb.classes_, index=df.index).astype(int)  # Ensure same index and convert to int
    
    # Concatenate the original DataFrame with the new encoded DataFrame
    df = pd.concat([df, column_encoded_df], axis=1)
    
    # Optionally, drop the original column if you no longer need it
    df = df.drop(column, axis=1)
    
    return df

def calculate_roi(revenue:float, budget:float) -> float:
    net_profit = revenue - budget
    roi = (net_profit / budget) * 100
    return roi

df = pd.read_csv('../data/tmdb/combined_tmdb_data.csv')
df = df.dropna(subset=['release_date', 'genres', 'budget', 'revenue'])
df = df[df['genres'] != '[]']  # Drop rows where 'genres' is an empty list

df['overview'] = df['overview'].fillna('No overview')
df['tagline'] = df['tagline'].fillna('No tagline')

# convert release_date to month and year
df['release_date'] = pd.to_datetime(df['release_date'])
df['release_month'] = df['release_date'].dt.month
df['release_year'] = df['release_date'].dt.year
df = df.drop('release_date', axis=1)

# drop columns:
# drop 'production_companies' for now -- too many unique values
df = df.drop('production_companies', axis=1)
# drop 'imdb_id' -- meaningless
df = df.drop('imdb_id', axis=1)
# dropping unhelpful movie-specific information (for regression anyway)
df = df.drop('original_title', axis=1)
df = df.drop('overview', axis=1)
df = df.drop('tagline', axis=1)
df = df.drop('title', axis=1)
df = df.drop('id', axis=1)
# dropping popularity metrics
df = df.drop('popularity', axis=1)
df = df.drop('vote_count', axis=1)
df = df.drop('vote_average', axis=1)

# one-hot encode categorical columns:
df = one_hot_encode_list('genres', df)
df = one_hot_encode_list('production_countries', df)
df = one_hot_encode_list('spoken_languages', df)
df = one_hot_encode_single('original_language', df)
df = one_hot_encode_single('status', df)

df['adult'] = df['adult'].astype(int)

df = df.loc[df['budget'].notnull()]  # Assuming 'budget' should never be null based on your preprocessing

df = df[[col for col in df.columns if re.match(r'^[\w\s]+$', col)]]

# Add 'roi' column and calculate ROI for every row
df['roi'] = calculate_roi(df['revenue'], df['budget'])

# Convert the dtypes Series to a DataFrame
types_df = pd.DataFrame(df.dtypes, columns=['Type']).reset_index()
# Rename 'index' column to 'Column' for clarity
types_df = types_df.rename(columns={'index': 'Column'})
# Iterate through the DataFrame and print each row
for index, row in types_df.iterrows():
    print(f"{row['Column']}: {row['Type']}")
    #if row['Type'] == 'object':
        #print(f"{row['Column']}: {row['Type']}")

df.to_csv('../data/tmdb/processed_tmdb_data.csv', index=False)


