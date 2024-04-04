import csv
from datetime import datetime

def calculate_gender_ratio(actors_data):
    total_actors = len(actors_data)
    female_actors = sum(1 for actor in actors_data if actor['gender'] == 1)
    if total_actors == 0:
        return 0
    return female_actors / total_actors

def calculate_average_age(actors_data, release_date):
    total_actors = len(actors_data)
    if total_actors == 0:
        return 0
    total_age = sum(release_date.year - actor['birth_year'] for actor in actors_data)
    return total_age / total_actors

def process_csv(input_file, output_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames + ['Gender Ratio', 'Average Actor Age']
        
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in reader:
                actors_data = []
                actor_birthdays = eval(row['actor_birthdays'])
                for i in range(5):
                    actor_gender_str = row[f'actor_{i}_gender']
                    if(actor_gender_str == ''): continue
                    actor_gender = int(float(actor_gender_str))
                    if actor_gender == 1 or actor_gender == 2:
                        if(actor_birthdays[i] == None): continue
                        actor_birthdate = datetime.strptime(actor_birthdays[i], '%Y-%m-%d')
                        if(row['release_year'] == ''): continue
                        release_year = int(float(row['release_year']))
                        actor_age = release_year - actor_birthdate.year
                        actors_data.append({'gender': actor_gender, 'birth_year': actor_birthdate.year})
                
                gender_ratio = calculate_gender_ratio(actors_data)
                row['Gender Ratio'] = gender_ratio
                if(row['release_year'] !=''):  
                    average_age = calculate_average_age(actors_data, datetime(int(float(row['release_year'])), int(float(row['release_month'])), 1))
                    row['Average Actor Age'] = average_age
                else:
                    row['Average Actor Age'] = -1
                writer.writerow(row)

# Example usage:
process_csv('/Users/hridayc/Desktop/eecs_448/box_office_busters/data/super_regression/modified_output.csv', 'mod_hriday.csv')
