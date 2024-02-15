import pandas as pd

def load_movie_data():
    # Define the path to the CSV file
    file_path = '../data/imdb/horror.csv'
    
    # Load the data into a pandas DataFrame
    horror_movies_df = pd.read_csv(file_path)
    
    return horror_movies_df

if __name__ == '__main__':
    # Load the movie data
    df = load_movie_data()
    
    # Display the first few rows of the DataFrame
    print(df.head())
