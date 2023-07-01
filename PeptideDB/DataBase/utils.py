
from datetime import datetime
import os
import json

def Version(version_string):
    today = datetime.today()
    formatted_date = today.strftime("%d:%m:%Y")
    
    major, minor, patch = version_string.split('.')
    major, minor, patch = int(major), int(minor), int(patch)
    if patch < 10:
        patch = patch+1
    else:
        patch = 0
        if  minor < 10:
            minor = minor+1
        else:
            minor = 0
            major = major+1

    return {'version':f"{major}.{minor}.{patch}", 'release_date':formatted_date}

def write_metadata_json():

    with open(os.path.join(os.getcwd(), 'metadata.json'), 'r') as file:
        json_data = json.load(file)

    # Manipulate the data

    m = Version(json_data['version'])

    print(m)
    json_data['version'] = m['version']
    json_data['release_date'] = m['release_date']



    # Write back to JSON file
    with open(os.path.join(os.getcwd(), 'metadata.json'), 'w') as file:
        json.dump(json_data, file, indent=4)



def return_metadata():

    with open(os.path.join(os.getcwd(), 'metadata.json'), 'r') as file:
        json_data = json.load(file)

    return json_data