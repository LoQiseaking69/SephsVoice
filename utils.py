
import json
import os

def load_json_file(file_path):
    if file_path and os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}

def save_json_file(data, file_path):
    if file_path:
        with open(file_path, 'w') as file:
            json.dump(data, file)

# Additional utility functions can be added here
