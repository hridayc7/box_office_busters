import csv
import requests
from tqdm import tqdm

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmM2EzYjE0YmJkYzY5MjcyZmNiMDUwZDI3M2Y3Mjc3ZCIsInN1YiI6IjY1YzZjNjQ0NjgwYmU4MDE3ZWEzNDhhMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.NZeryWwYxMP1qjN0Stw33lF7cPmnJBuwmPmguIiIvMs"
}

def extract_movie_info(json_data):
    movie_info = {}
    
    # Extracting information from JSON
    movie_info['adult'] = json_data.get('adult', False)  # Default value if 'adult' key doesn't exist
    movie_info['belongs_to_collection'] = bool(json_data.get('belongs_to_collection', False))  # Default value if 'belongs_to_collection' key doesn't exist
    if json_data.get('belongs_to_collection'):
        movie_info['collection_id'] = json_data['belongs_to_collection'].get('id', None)  # Default value if 'id' key doesn't exist
    movie_info['budget'] = json_data.get('budget', None)  # Default value if 'budget' key doesn't exist
    movie_info['genres'] = [genre['name'] for genre in json_data.get('genres', [])]  # Default value if 'genres' key doesn't exist or is empty
    movie_info['overview'] = json_data.get('overview', '')  # Default value if 'overview' key doesn't exist
    if json_data.get('production_companies'):
        movie_info['production_company_id'] = json_data['production_companies'][0].get('id', None)  # Default value if 'id' key doesn't exist
        movie_info['production_company_name'] = json_data['production_companies'][0].get('name', '')  # Default value if 'name' key doesn't exist
    else:
        movie_info['production_company_id'] = None
        movie_info['production_company_name'] = ''
    if 'release_date' in json_data:
        if(json_data['release_date'] != ""):
            try:
                release_date_parts = json_data['release_date'].split('-')
                movie_info['release_month'] = int(release_date_parts[1]) if len(release_date_parts) > 1 else None  # Default value if 'release_date' key doesn't exist or is in invalid format
                movie_info['release_year'] = int(release_date_parts[0]) if len(release_date_parts) > 0 else None  # Default value if 'release_date' key doesn't exist or is in invalid format
            except Exception as e:
                print(f"Error processing release date parts for TMDB ID: {json_data.get('id')}")
                print(f"Release date parts: {release_date_parts}")
                print(f"Error message: {str(e)}")
                movie_info['release_month'] = None
                movie_info['release_year'] = None
    else:
        movie_info['release_month'] = None
        movie_info['release_year'] = None
    movie_info['revenue'] = json_data.get('revenue', None)  # Default value if 'revenue' key doesn't exist
    movie_info['tagline'] = json_data.get('tagline', '')  # Default value if 'tagline' key doesn't exist
    movie_info['tmdb_id'] = json_data.get('id', None)  # Default value if 'id' key doesn't exist

    return movie_info



def get_top_level_details(tmdb_id):
    # URL for the TMDB API
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?language=en-US"

    # Make a GET request to the TMDB API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Get movie data
        return extract_movie_info(response.json())

    else:
        print("Error:", response.status_code)


import csv
from tqdm import tqdm

def process_csv(csv_file):
    # maps tmdb ids to movie_info "struct"
    movie_map = {}

    # Open the CSV file in read mode
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        # Create a CSV reader object
        reader = csv.reader(file)
        
        # Skip the header row
        next(reader)
        
        # Wrap the iteration with tqdm for progress tracking
        for row in tqdm(reader, desc="Processing CSV", unit=" rows"):
            # Extract the TMDB ID from the first column (index 0)
            tmdb_id = row[0]
            movie_map[tmdb_id] = get_top_level_details(tmdb_id)

    # Write movie_map to a CSV file
    output_file = 'output.csv'
    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['tmdb_id', 'adult', 'belongs_to_collection', 'collection_id', 'budget', 'genres', 'overview', 'production_company_id', 'production_company_name', 'release_month', 'release_year', 'revenue', 'tagline']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Write movie_map values
        for tmdb_id, movie_info in movie_map.items():
            if movie_info is not None:
                writer.writerow(movie_info)
            else:
                print(f"Movie info for TMDB ID {tmdb_id} is None. Skipping writing to CSV.")

    return movie_map

            
def main():
    # Define the path to your CSV file
    csv_file = '../data/tmdb_ids.csv'
    
    # Call the function to process the CSV file
    movie_map = process_csv(csv_file)
    print(movie_map)

if __name__ == "__main__":
    main()
