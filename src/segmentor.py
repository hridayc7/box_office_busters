import os
import csv

# Function to create a directory if it doesn't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to segment the CSV file and write to separate files
def segment_csv(csv_file, num_segments):
    # Create a directory to store segmented CSV files
    directory = os.path.splitext(csv_file)[0] + "_segmented"
    create_directory(directory)

    # Open the CSV file for reading
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header

        # Initialize segment counters and CSV writers
        segment_size = 1000 // num_segments
        current_segment = 1
        current_segment_count = 0
        output_file = None

        for row in reader:
            # Check if it's time to start a new segment
            if current_segment_count == 0:
                # Close the previous output file
                if output_file:
                    output_file.close()

                # Open a new output file for writing
                output_file_name = os.path.join(directory, f"segment_{current_segment}.csv")
                output_file = open(output_file_name, mode='w', newline='', encoding='utf-8')
                writer = csv.writer(output_file)

                # Write the header
                writer.writerow(header)

                # Increment segment counter
                current_segment += 1

            # Write the row to the current segment
            writer.writerow(row)
            current_segment_count += 1

            # Check if the segment size limit has been reached
            if current_segment_count >= segment_size:
                current_segment_count = 0

        # Close the last output file
        if output_file:
            output_file.close()

    print(f"CSV file segmented into {num_segments} files in directory: {directory}")

def main():
    csv_file = '/Users/hridayc/Developer/box_office_busters/data/tmdb/combined_tmdb_data.csv'  # Change this to the path of your CSV file
    num_segments = 1
    segment_csv(csv_file, num_segments)

if __name__ == "__main__":
    main()
