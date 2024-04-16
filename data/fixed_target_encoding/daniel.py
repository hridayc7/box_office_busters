import pandas as pd
from tqdm import tqdm

# Assuming your data is stored in a DataFrame called 'movies_df'
file_path = 'No_Encodings.csv'
movies_df = pd.read_csv(file_path)

# Create empty lists to store the new columns
actor0_rev = []
actor0_movies = []
actor1_rev = []
actor1_movies = []
actor2_rev = []
actor2_movies = []

# Wrap the main loop with tqdm for progress tracking
for index, row in tqdm(movies_df.iterrows(), total=len(movies_df), desc="Processing movies"):
    # Extract actor names
    actor_names = [row['actor_0_name'],
                   row['actor_1_name'], row['actor_2_name']]
    release_year = row['release_year']
    release_month = row['release_month']
    # Initialize variables to store total revenue and number of movies for each actor
    actor0_total_rev = 0
    actor0_total_movies = 0
    actor1_total_rev = 0
    actor1_total_movies = 0
    actor2_total_rev = 0
    actor2_total_movies = 0

    # Iterate through each previous movie to calculate total revenue and number of movies for each actor
    for i in range(len(actor_names)):
        actor_name = actor_names[i]
        # Filter movies released before the current movie
        previous_movies = movies_df[(movies_df['release_year'] < release_year) |
                                    ((movies_df['release_year'] == release_year) & (movies_df['release_month'] < release_month))]
        # Check if the actor appeared in any previous movies
        actor_previous_movies = previous_movies[(previous_movies['actor_0_name'] == actor_name) |
                                                (previous_movies['actor_1_name'] == actor_name) |
                                                (previous_movies['actor_2_name'] == actor_name)]
        # Calculate total revenue and number of movies for the actor
        actor_total_rev = actor_previous_movies['revenue'].sum()
        actor_total_movies = len(actor_previous_movies)
        # Assign the calculated values to the corresponding actor
        if i == 0:
            actor0_total_rev = actor_total_rev
            actor0_total_movies = actor_total_movies
        elif i == 1:
            actor1_total_rev = actor_total_rev
            actor1_total_movies = actor_total_movies
        elif i == 2:
            actor2_total_rev = actor_total_rev
            actor2_total_movies = actor_total_movies

    # Append the calculated values to the lists
    actor0_rev.append(actor0_total_rev)
    actor0_movies.append(actor0_total_movies)
    actor1_rev.append(actor1_total_rev)
    actor1_movies.append(actor1_total_movies)
    actor2_rev.append(actor2_total_rev)
    actor2_movies.append(actor2_total_movies)

# Add the new columns to the DataFrame
movies_df['actor0_rev'] = actor0_rev
movies_df['actor0_movies'] = actor0_movies
movies_df['actor1_rev'] = actor1_rev
movies_df['actor1_movies'] = actor1_movies
movies_df['actor2_rev'] = actor2_rev
movies_df['actor2_movies'] = actor2_movies

# Save the DataFrame to a CSV file named "Daniel.csv"
movies_df.to_csv("Daniel.csv", index=False)
