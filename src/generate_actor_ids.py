import json

def generate_dictionaries(file_path):
    # Read names from the given file
    with open(file_path, 'r') as file:
        names = file.read().splitlines()
    
    # Generate the mappings
    name_to_id = {name: idx for idx, name in enumerate(names, start=1)}
    id_to_name = {idx: name for name, idx in name_to_id.items()}
    
    # Save the dictionaries to JSON files
    with open('name_to_id.json', 'w') as file:
        json.dump(name_to_id, file)
    
    with open('id_to_name.json', 'w') as file:
        json.dump(id_to_name, file)

file_path = '../data/tmdb/all_actors.txt'
generate_dictionaries(file_path)