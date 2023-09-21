
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


def upload_data_from_backup_file(file_path):

    with open(file_path) as f:
        data = json.load(f)
   
    for i in data:
        if "DataBase.peptideseq" == i['model']:
            if not PeptideSeq.objects.filter( 
                    accession=chunks[0],
                    gene_symbol=chunks[1],
                    protein_name=chunks[2],
                    cleavage_site=chunks[3],
                    peptide_sequence=chunks[4],
                    annotated_sequence=chunks[5],
                    cellular_compartment=chunks[6],
                    species=chunks[7],
                    database_identified=chunks[8],
                    description=chunks[9],
                    reference_number=ref_num,
                    reference_link=ref_link,

                ).exists():

                new_obj = PeptideSeq.objects.create(

                    db_id='DBS0'+str(count),
                    accession=chunks[0],
                    gene_symbol=chunks[1],
                    protein_name=chunks[2],
                    cleavage_site=chunks[3],
                    peptide_sequence=chunks[4],
                    annotated_sequence=chunks[5],
                    cellular_compartment=chunks[6],
                    species=chunks[7],
                    database_identified=chunks[8],
                    description=chunks[9],
                    reference_number=ref_num,
                    reference_link=ref_link,
                    data_file_name= file_name
                )

                new_obj.save()
        
        elif "DataBase.uploadeddata" == i['model']:
            if not PeptideSeq.objects.filter (

                    datafile_index = i['datafile_index'],
                    experiment_name = i['experiment_name'],
                    data_upload_time = i['data_upload_time'],
                    data_upload_date = i['data_upload_date'],
                    user_name = i['user_name'],
                    data_description = i['data_description'],
                    data_file_name = i['data_file_name'],
                    experiment_type = i['experiment_type'],
                    reference_number = i['reference_number'],
                    reference_link = i['reference_link'],
                ).exists():

                uploaded_data_object = PeptideSeq.objects.create (

                    datafile_index = i['datafile_index'],
                    experiment_name = i['experiment_name'],
                    data_upload_time = i['data_upload_time'],
                    data_upload_date = i['data_upload_date'],
                    user_name = i['user_name'],
                    data_description = i['data_description'],
                    data_file_name = i['data_file_name'],
                    experiment_type = i['experiment_type'],
                    reference_number = i['reference_number'],
                    reference_link = i['reference_link'],
                )

                uploaded_data_object.save()

    
        elif "DataBase.bugreporting" == i['model']:
            if not BugReporting.objects.filter(
                title = i['title'],
                report_date = i['report_date'],
                report_time = i['report_time'],
                bug_description = i['bug_description'],
                user_name = i['user_name'],
                institute = i['institute'],
                email  = i['email'],
                types = i['types'],
                ).exists():

                br = BugReporting.objects.create(
                    title = i['title'],
                    report_date = i['report_date'],
                    report_time = i['report_time'],
                    bug_description = i['bug_description'],
                    user_name = i['user_name'],
                    institute = i['institute'],
                    email  = i['email'],
                    types = i['types'],
                )

                br.save()

        elif "DataBase.databaseversion" == i['model']:
            if not DataBaseVersion.objects.filter(
                version = i['version'],
                time_stamp = i['time_stamp'],
                ).exists():

                dbv = DataBaseVersion.objects.create(
                    version = i['version'],
                    time_stamp = i['time_stamp'],
                )

                dbv.save()

        elif "DataBase.file" == i['model']:
            if not File.objects.filter(
                existingPath = i['existingPath'],
                name = i['path'],
                eof = i['eof'],
                ).exists():

                fl = File.objects.create(
                    existingPath = i['existingPath'],
                    name = i['path'],
                    eof = i['eof'],
                )

                fl.save()