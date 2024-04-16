import pandas as pd

# Assuming df is your DataFrame containing the movie data
df = pd.read_csv('cleaned_movie_data.csv')
print("help!")
# Drop rows with NaN values
df.dropna(inplace=True)

# # Convert the 'actor_birthdays' column to datetime
# df['release_date'] = pd.to_datetime(df['release_year'].astype(int).astype(
#     str) + '-' + df['release_month'].astype(int).astype(str) + '-01')

# Initialize new columns for encoded actor names
for i in range(3):
    df[f'actor_{i}_name_encoded'] = 0

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    # Get the revenues of movies each actor has been in
    actor_revenues = df[(df['release_date'] < row['release_date']) &
                        (df[f'actor_{i}_name'] == row[f'actor_{i}_name'])]['revenue']

    if (df[f'actor_{i}_name'] == "Daniel Radcliffe"):
        print("Break")

    # Calculate the average revenue for each actor
    for i in range(3):
        actor_avg_revenue = actor_revenues.mean() if not actor_revenues.empty else 0
        df.at[index, f'actor_{i}_name_encoded'] = actor_avg_revenue

# Display the DataFrame with the new encoded columns
print(df)

# Write the DataFrame to a CSV file
df.to_csv('encoded.csv', index=False)
