import os
from .forms import  dabase_form, UploadFileForm, BugReportingForm
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, JsonResponse,  HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime
from .models import UploadedData, BugReporting, PeptideSeq, DataBaseVersion, File
from django.core import serializers
import pandas as  pd
import json
from .utils import write_metadata_json, return_metadata, time_stamp
from io import StringIO
from django.core.management import call_command
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
# from .utils import return_merge_peptidedata
from pathlib import Path
from django.conf import settings


base_dir = settings.MEDIA_ROOT

def errors(request):
    return render(request, 'DataBase/error.html')

def contact(request):
    logout(request)
    return render(request, 'DataBase/contact.html', {})

def DB(request):
    if len(DataBaseVersion.objects.all()) == 0:
        v = DataBaseVersion.objects.create(
            version = '0.0.0' ,
            time_stamp = time_stamp(),
        )

        v.save()

    acv = len(set(list(PeptideSeq.objects.filter(accession__isnull=False).values_list('accession', flat=True))))
    clv = len((list(PeptideSeq.objects.filter(cleavage_site__isnull=False).values_list('cleavage_site', flat=True))))

    if request.method == 'POST':
        form = dabase_form(request.POST)
        formb = BugReportingForm(request.POST)

        if form.is_valid():
            description = form.cleaned_data['Sequence']
            accession = form.cleaned_data['Accession']

            if description != '' and accession != '':
                param = {'acc':accession,'des':description, 'host_name':  request.get_host()}
                return render(request, 'DataBase/table.html', param)
            elif description == '' and accession != '':                
                param = {'acc':accession,'des':'undefined', 'host_name':  request.get_host()}
                return render(request, 'DataBase/table.html', param)
            elif accession == '' and description != '':
                param = {'acc':'undefined','des':description, 'host_name':  request.get_host()}
                return render(request, 'DataBase/table.html', param)

            elif description == '' and accession == '':
                render(request, 'DataBase/index.html', {'form': form, 'acv':acv, 'clv':clv, 'formb':formb, 'is_authenticated':request.user.is_authenticated, 'host_name': request.get_host()})

        elif formb.is_valid():

            now = datetime.now()
            a = BugReporting.objects.create(
                title = formb.cleaned_data['title'],
                report_date = now.strftime("%Y-%m-%d"),
                report_time = now.strftime("%H:%M:%S"),
                bug_description = formb.cleaned_data['bug_description'],
                user_name  =  formb.cleaned_data['user_name'],
            )
            a.save()

            return HttpResponseRedirect('/success')

    else:
        Fasta = ''
        Acc = ''
        form = dabase_form(initial={'Sequence':Fasta,'Accession':Acc})
        
    meta_data = DataBaseVersion.objects.latest('time_stamp')

    if len(DataBaseVersion.objects.all()) == 0:
        now = datetime.now()
        new_obj = DataBaseVersion.objects.create(
                version='0.0.0',
                time_stamp= now.strftime("%Y-%m-%d"),
            )
        new_obj.save()


    meta_data = {
                "version": DataBaseVersion.objects.latest('time_stamp').version,
                "release_date": DataBaseVersion.objects.latest('time_stamp').time_stamp.split('.')[0],
                }

    return render(request, 'DataBase/index.html', {'form': form, 'acv':acv, 'clv':clv, 'meta_data':meta_data, 'is_authenticated':request.user.is_authenticated, 'host_name': request.get_host()})

@staff_member_required
def data_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            now = datetime.now()
            dt_string = now.strftime("%d_%m_%Y__%H_%M_%S")
            file_name = "CleavageDB_"+dt_string+'_data_file.csv'
            # objs = UploadedData.objects.all()
            validation_pass = handle_uploaded_file(request, request.FILES['file'], file_name, form.cleaned_data['reference_number'], form.cleaned_data['reference_link'])

            if validation_pass['validation']:
                a = UploadedData.objects.create(
                    datafile_index='DBF'+str(len(UploadedData.objects.all())),
                    experiment_name=form.cleaned_data['experiment_name'],
                    data_upload_date=now.strftime("%Y-%m-%d"),
                    data_upload_time=now.strftime("%H:%M:%S"),
                    user_name=form.cleaned_data['user'],
                    data_description=form.cleaned_data['description'],
                    data_file_name=file_name,
                    experiment_type=form.cleaned_data['experiment_type'],
                    reference_number=form.cleaned_data['reference_number'],
                    reference_link=form.cleaned_data['reference_link'],
                    )
                a.save()

                return HttpResponseRedirect('/data_upload')
            else:
                return render(request, 'DataBase/validation_error.html', {'data': validation_pass['error_column'] })
    else:
        form = UploadFileForm()
    return render(request, 'DataBase/upload.html', {'form': form})
  
def handle_uploaded_file(request, f, file_name, ref_number, ref_link):

    headers = ['Protein Accession', 'Gene symbol', 'Protein name', 'Cleavage site', 'Peptide sequence',	'Annotated sequence', 'Cellular Compartment',	'Species','Database identified', 'Discription', 'Reference']
    line = f.readline().decode('UTF-8')

    for i, h in enumerate(line.replace('\r\n', '').split('\t')):
        if h == headers[i]:
            pass
        else:
            return {"validation": False, "error_column": h}
    
    directory_path = os.path.join(str(settings.BASE_DIR), 'media', 'datafiles')
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    with open(os.path.join(settings.BASE_DIR, 'media', 'datafiles', file_name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    import_data_to_model(file_name, ref_number, ref_link)
    return {'validation': True}
    
def bugs(request):

    data = request.GET.get('data', {})
    now = datetime.now()
    data =  json.loads(data)

    a = BugReporting.objects.create(

        title = data['title'],
        report_date = now.strftime("%Y-%m-%d"),
        report_time = now.strftime("%H:%M:%S"),
        bug_description = data['details'],
        types = data['type']
    )
    a.save()

    return JsonResponse(data, safe=False)  
    # return render(request, 'DataBase/bug_report_form.html', {'form': form})

def success(request):
    return render(request,  'DataBase/bug_submission_success.html', {})

@staff_member_required
def download_data_report(request):
    return render(request,  'DataBase/uploaded_data_report.html', {})

def import_data_to_model(file_name, ref_num, ref_link):
    f = open(os.path.join(settings.BASE_DIR, 'media', 'datafiles', file_name))
    lines = f.readlines()

    print(lines)

    count = PeptideSeq.objects.all().count()
    start = count
    for line in lines[1:]:
        chunks = line.split('\t')
        # print(chunks)
        # num_of_obj = PeptideSeq.objects.filter(
        #     sequence=chunks[0],
        #     master_protein_accession=chunks[1],
        #      master_protein_description=chunks[2],
        #     cleavage_site=chunks[3],
        #     annotated_sequence=chunks[4],
        #     abundance=chunks[5],
        # ).count()

        # if num_of_obj > 0:
        #     pass
        # else:

        count = count + 1

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
        else:
            pass

    now = datetime.now()
    vsn = DataBaseVersion.objects.latest('time_stamp')
    count_end = PeptideSeq.objects.all().count()

    if count_end != start:
        updated_version = DataBaseVersion.objects.latest('time_stamp')
        w = write_metadata_json(updated_version.version)

        v = DataBaseVersion.objects.create(
            version = w['version'] ,
            time_stamp = w['release_date'],
        )

        v.save()
    
def PepView(request):
    data = {}

    if 'des' in request.GET and 'acc' in request.GET :
        record = PeptideSeq.objects.filter(protein_name__contains=request.GET['des'], accession__contains=request.GET['acc'])
        qs = serializers.serialize('json', record)
        qs_json = return_merge_peptidedata(json.loads(qs))
        return JsonResponse(qs_json, safe=False)

    elif  'acc' in request.GET and 'des' not in request.GET:
        record = PeptideSeq.objects.filter( accession__contains=request.GET['acc'])
        qs = serializers.serialize('json', record)
        qs_json = return_merge_peptidedata(json.loads(qs))

        return JsonResponse(qs_json, safe=False)

    elif 'des' in request.GET  and 'acc' not in request.GET:
        record = PeptideSeq.objects.filter(protein_name__contains=request.GET['des'])
        qs = serializers.serialize('json', record)
        qs_json = return_merge_peptidedata(json.loads(qs))
        return JsonResponse(qs_json, safe=False)

def references(request):
    return render(request, 'DataBase/references.html', {})

def data_validation_error(request):
    return render(request, 'DataBase/validation_error.html')

def test_view(request):
    return render(request, 'DataBase/table_1.html')

@staff_member_required
def top_bugs(request):
    bugs = BugReporting.objects.all().order_by('-report_date').order_by('-report_time')
    return render(request, 'DataBase/bug_list.html', {'bugs': bugs})

def return_merge_peptidedata(retrived_peps):
    
    """
    this function takes input from django query and 
    merges dublicate protein entries. 
    
    """
    pep_set = []

    for p in retrived_peps:
        pep_set.append(p['fields']['peptide_sequence'])

    updated_pep_records = []

    for pep in set(pep_set):
        db_id = []
        accession= []
        gene_symbol=[] 
        protein_name=[]
        cleavage_site=[]
        peptide_sequence=[]
        annotated_sequence=[] 
        cellular_compartment=[] 
        species=[] 
        database_identified=[] 
        description=[]
        reference_number=[]
        reference_link=[]
        data_file_name=[]

        for record in retrived_peps:
            if pep == record['fields']['peptide_sequence']:

                db_id.append(record['fields']['db_id'])
                accession.append(record['fields']['accession'])
                gene_symbol.append(record['fields']['gene_symbol'])
                protein_name.append(record['fields']['protein_name'])
                cleavage_site.append(record['fields']['cleavage_site'])
                peptide_sequence.append(record['fields']['peptide_sequence'])
                annotated_sequence.append(record['fields']['annotated_sequence'])
                cellular_compartment.append(record['fields']['cellular_compartment'])
                species.append(record['fields']['species'])
                database_identified.append(record['fields']['database_identified'])
                description.append(record['fields']['description'])
                reference_number.append(record['fields']['reference_number'])
                reference_link.append(record['fields']['reference_link'])
                data_file_name.append(record['fields']['data_file_name'])

        updated_pep_record = {
                            
                            'db_id':", ".join(list(set(db_id))), 
                            'accession':", ".join(list(set(accession))),
                            'gene_symbol':", ".join(list(set(gene_symbol))), 
                            'protein_name':", ".join(list(set(protein_name))), 
                            'cleavage_site':", ".join(list(set(cleavage_site))), 
                            'peptide_sequence':", ".join(list(set(peptide_sequence))), 
                            'annotated_sequence':", ".join(list(set(annotated_sequence))), 
                            'cellular_compartment':", ".join(list(set(cellular_compartment))), 
                            'species':", ".join(list(set(species))), 
                            'database_identified':", ".join(list(set(database_identified))), 
                            'description':", ".join(list(set(description))), 
                            'reference_number':list(set(reference_number)), 
                            'reference_link':list(set(reference_link)), 
                            'data_file_name':", ".join(list(set(data_file_name))),
                        }

        updated_pep_records.append(updated_pep_record)

    return updated_pep_records

@staff_member_required
def user_activity(request):

    bugs =  BugReporting.objects.all().filter(types="bug")
    suggestions = BugReporting.objects.all().filter(types="suggestion")
    db =  len(PeptideSeq.objects.all())

    n_bugs = len(bugs)
    n_suggestions = len(suggestions)
    metadata = DataBaseVersion.objects.latest('time_stamp')

    json_data = {
                "version": metadata.version,
                "release_date": metadata.time_stamp.split('.')[0],
                }

    return render(request, 'DataBase/user_activity.html', {'data':json_data, 'bugs':bugs, 'suggestions':suggestions, 'n_bugs':n_bugs, 'n_suggestions': n_suggestions, 'db':db, 'is_authenticated':True})

@staff_member_required
def bug_list(request):
    bugs =  BugReporting.objects.all().filter(types="bug")
    return render(request, 'DataBase/bug_list.html', {'bugs':bugs, 'is_authenticated':True})

@staff_member_required
def suggestion_list(request):
    suggestions = BugReporting.objects.all().filter(types="suggestion")
    return render(request, 'DataBase/suggestion_list.html', {'suggestions':suggestions, 'is_authenticated':True})

def logout_view(request):
    logout(request)
    return redirect('/') 

@staff_member_required
def load_data(request):
    return render(request, 'DataBase/load_data_from_backup_file.html', {})

@staff_member_required
def download_backup(request):

    h = DataBaseVersion.objects.latest('time_stamp')
    f_name = h.version.replace('.', '_')+"_back_up.json"

    output = StringIO()
    call_command('dumpdata', stdout=output)
    response = HttpResponse(output.getvalue(), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename='+f_name
    return response

@staff_member_required
def upload_backup(request):
    if request.method == 'POST' and request.FILES.get('backup_file'):
        backup_file = request.FILES['backup_file']
        call_command('loaddata', backup_file.temporary_file_path())
        messages.success(request, 'Data successfully restored!')
        return redirect('some_view_name')  # replace with a view name where you want to redirect after loading data
    return render(request, 'load_data_from_backup_file.html')
    
def fileUploader(request):
    if request.method == 'POST':  
        file = request.FILES['file'].read()
        fileName= request.POST['filename']
        existingPath = request.POST['existingPath']
        end = request.POST['end']
        nextSlice = request.POST['nextSlice']

        if file=="" or fileName=="" or existingPath=="" or end=="" or nextSlice=="":
            res = JsonResponse({'data':'Invalid Request'})
            return res
        else:
            if existingPath == 'null':

                directory_path = os.path.join(str(settings.BASE_DIR), 'media', 'backupdata')
                if not os.path.exists(directory_path):
                    os.makedirs(directory_path)

                path = os.path.join(directory_path, fileName)
                with open(path, 'wb+') as destination: 
                    destination.write(file)

                FileFolder = File()

                FileFolder.existingPath = fileName
                FileFolder.eof = end
                FileFolder.name = fileName

                try:
                    FileFolder.save()
                except:
                    return HttpResponseRedirect('/errors')
                if int(end):
                    res = JsonResponse({'data':'Uploaded Successfully','existingPath': fileName})
                else:
                    res = JsonResponse({'existingPath': fileName})
                return res

            else:
                path = 'backupdata/' + existingPath
                model_id = File.objects.get(existingPath=existingPath)
                if model_id.name == fileName:
                    if not model_id.eof:
                        with open(path, 'ab+') as destination: 
                            destination.write(file)
                        if int(end):
                            model_id.eof = int(end)
                            model_id.save()
                            res = JsonResponse({'data':'Uploaded Successfully','existingPath':model_id.existingPath})
                        else:
                            res = JsonResponse({'existingPath':model_id.existingPath})    
                        return res
                    else:
                        res = JsonResponse({'data':'EOF found. Invalid request'})
                        return res
                else:
                    res = JsonResponse({'data':'No such file exists in the existingPath'})
                    return res
    return render(request, 'load_data_from_backup_file.html')

def UploadedView(request):
    return render(request, 'DataBase/load_data_from_backup_file.html', {})

@csrf_exempt
def upload_chunk(request):

    file = request.FILES['file']

    file_id = request.POST['resumableIdentifier']
    chunk_number = request.POST['resumableChunkNumber']
    total_chunks = int(request.POST['resumableTotalChunks'])

    directory_path = os.path.join(str(settings.BASE_DIR), 'media', 'tmp')
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    
    with open(os.path.join(settings.BASE_DIR, 'media', 'tmp',file_id+"_"+chunk_number), 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)

    return JsonResponse({'status': 'success'})

@csrf_exempt
def merge_chunks(request):

    file_id = request.GET.get('file_id', None)
    total_chunck = request.GET.get('total_chunck', None)
    file_name = request.GET.get('file_name', None)


    directory_path = os.path.join(str(settings.BASE_DIR), 'media', 'uploads')
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    print("##################################################")
    print(os.path.join(settings.BASE_DIR, 'media', 'uploads'))
    print("##################################################")
  
    with open(os.path.join(settings.BASE_DIR, 'media', 'uploads', file_name), 'wb') as final_file:
        for i in range(1, int(total_chunck) + 1):
            with open(os.path.join(settings.BASE_DIR, 'media', 'tmp', file_id+'_'+str(i)), 'rb') as chunk:
                final_file.write(chunk.read())
            os.remove(os.path.join(settings.BASE_DIR, 'media', 'tmp', file_id+'_'+str(i)))

    return HttpResponseRedirect('/load_backupdata/?&file_name='+file_name)

@staff_member_required
def upload_page(request):
    return render(request, 'DataBase/backup_upload.html')

@staff_member_required
def upload_complete(request):
    file_name = request.GET.get('file_name', None)
    return render(request, 'DataBase/upload_complete.html', {'file_name': request.GET.get('file_name', None)})

@staff_member_required
def load_backupdata(request):
    file_name = request.GET.get('file_name', None)

    with open(os.path.join(settings.BASE_DIR, 'media', 'uploads', file_name), 'r') as file:
        data = json.load(file)

    p_count = PeptideSeq.objects.all().count()
    # b_count = BugReporting.objects.all().count()

    for i in data:
        if  'DataBase.peptideseq' == i['model']:

            # count = PeptideSeq.objects.all().count()
            p_count = p_count + 1

            if not PeptideSeq.objects.filter( 
                        accession=i['fields']['accession'],
                        gene_symbol=i['fields']['gene_symbol'],
                        protein_name=i['fields']['protein_name'],
                        cleavage_site=i['fields']['cleavage_site'],
                        peptide_sequence=i['fields']['peptide_sequence'],
                        annotated_sequence=i['fields']['annotated_sequence'],
                        cellular_compartment=i['fields']['cellular_compartment'],
                        species=i['fields']['species'],
                        database_identified=i['fields']['database_identified'],
                        description=i['fields']['description'],
                        reference_number=i['fields']['reference_number'],
                        reference_link=i['fields']['reference_link'],
                        # data_file_name= i['fields']['data_file_name'],

                ).exists():

                new_obj = PeptideSeq.objects.create(

                    db_id='DBS0'+str(p_count),
                    accession=i['fields']['accession'],
                    gene_symbol=i['fields']['gene_symbol'],
                    protein_name=i['fields']['protein_name'],
                    cleavage_site=i['fields']['cleavage_site'],
                    peptide_sequence=i['fields']['peptide_sequence'],
                    annotated_sequence=i['fields']['annotated_sequence'],
                    cellular_compartment=i['fields']['cellular_compartment'],
                    species=i['fields']['species'],
                    database_identified=i['fields']['database_identified'],
                    description=i['fields']['description'],
                    reference_number=i['fields']['reference_number'],
                    reference_link=i['fields']['reference_link'],
                    data_file_name= file_name,
                    # data_file_name= i['fields']['file_name'],
                )

                new_obj.save()
            else:
                pass

        elif 'DataBase.bugreporting' == i['model']:

            if not BugReporting.objects.filter( 
                        title=i['fields']['title'],
                        report_date=i['fields']['report_date'],
                        report_time=i['fields']['report_time'],
                        bug_description=i['fields']['bug_description'],
                        types=i['fields']['types'],

                ).exists():

                new_obj = BugReporting.objects.create(
                        title=i['fields']['title'],
                        report_date=i['fields']['report_date'],
                        report_time=i['fields']['report_time'],
                        bug_description=i['fields']['bug_description'],
                        types=i['fields']['types'],
                )

                new_obj.save()
            else:
                pass

        elif 'databaseversion' in i['model']:
          
            if not DataBaseVersion.objects.filter( 
                        version=i['fields']['version'],
                        # time_stamp=i['fields']['time_stamp'],

                ).exists():

                new_obj = DataBaseVersion.objects.create(
                        version=i['fields']['version'],
                        time_stamp=i['fields']['time_stamp'],
                )

                new_obj.save()
            else:
                pass

        elif 'DataBase.file' == i['model']:
            if not File.objects.filter( 
                        name=i['fields']['name'],
                ).exists():

                new_obj = PeptideSeq.objects.create(
                    name=i['fields']['name'],
                )

                new_obj.save()
            else:
                pass


    os.remove(os.path.join(base_dir, 'uploads', file_name))

    return render(request, 'DataBase/upload_complete.html', {})
