import csv

# Function to remove movies with budget or revenue <= 10


def filter_movies(input_file):
    filtered_movies = []
    with open(input_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            budget = float(row['budget'])
            revenue = float(row['revenue'])
            if budget > 10 and revenue > 10:
                filtered_movies.append(row)
    return filtered_movies

# Function to get runtime for each movie


def get_runtime(filtered_movies, combined_data_file):
    movie_runtimes = {}
    with open(combined_data_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tmdb_id = int(float(row['id']))
            runtime = float(row['runtime'])
            movie_runtimes[tmdb_id] = runtime

    for movie in filtered_movies:
        tmdb_id = int(movie['tmdb_id'])
        if tmdb_id in movie_runtimes:
            movie['runtime'] = movie_runtimes[tmdb_id]

    return filtered_movies

# Function to write filtered data to a new CSV file


def write_to_csv(filtered_data, output_file):
    fieldnames = filtered_data[0].keys()
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_data)

# Main function to execute the script


def main():
    # Input files
    filtered_data_file = '../data/super_regression/filtered_data.csv'
    combined_data_file = '../data/tmdb/combined_tmdb_data.csv'

    # Output file
    output_file = 'april.csv'

    # Step 1: Remove movies with budget or revenue <= 10
    filtered_movies = filter_movies(filtered_data_file)

    # Step 2: Get runtime for each movie
    filtered_movies_with_runtime = get_runtime(
        filtered_movies, combined_data_file)

    # Step 3: Write filtered data with runtime to a new CSV file
    write_to_csv(filtered_movies_with_runtime, output_file)

    print("Filtered data with runtime has been saved to:", output_file)


if __name__ == "__main__":
    main()
