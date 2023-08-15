
from datetime import datetime
import os
import json
import pytz

def Version(version_string):
    today = datetime.today()
    formatted_date = time_stamp()
    
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

def write_metadata_json(version):

    json_data = {'version':None, 'release_date':None}
    m = Version(version)

    json_data['version'] = m['version']
    json_data['release_date'] = m['release_date']

    return json_data

def return_metadata():

    with open(os.path.join(os.getcwd(), 'metadata.json'), 'r') as file:
        json_data = json.load(file)

    return json_data

def time_stamp():
    utc_time = datetime.now(pytz.utc)
    local_time_zone = pytz.timezone('America/New_York')
    local_time = utc_time.astimezone(local_time_zone)
    return str(local_time)