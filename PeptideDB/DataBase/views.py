from django.shortcuts import render
from .forms import  dabase_form, UploadFileForm, BugReportingForm
from django.contrib.auth import logout
import os
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime
from .models import UploadedData, BugReporting, PeptideSeq
from django.core import serializers
import pandas as  pd
import json

# from .utils import return_merge_peptidedata

def contact(request):
    logout(request)
    return render(request, 'DataBase/contact.html', {})

def DB(request):

    if request.method == 'POST':
        form = dabase_form(request.POST)

        if form.is_valid():

            description = form.cleaned_data['Sequence']
            accession = form.cleaned_data['Accession']
            if description != '' and accession != '':
                param = {'acc':accession,'des':description, 'host_name':  request.get_host()}
                return render(request, 'DataBase/data-table.html', param)
            elif description == '' and accession != '':                
                param = {'acc':accession,'des':'undefined', 'host_name':  request.get_host()}
                return render(request, 'DataBase/data-table.html', param)
            elif accession == '' and description != '':
                param = {'acc':'undefined','des':description, 'host_name':  request.get_host()}
                return render(request, 'DataBase/data-table.html', param)

            elif description == '' and accession == '':
                render(request, 'DataBase/base.html', {'form': form})
    else:
        Fasta = ''
        Acc = ''
        form = dabase_form(initial={'Sequence':Fasta,'Accession':Acc})
        
    logout(request)
    return render(request, 'DataBase/db_query_form.html', {'form': form})

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

    headers = ['Protein Accession', 'Gene symbol', 'Protein name', 'Cleavage site', 'Peptide sequence',	'Annotated sequence', 'Cellular Compartment',	'Species', 'Database identified', 'Discription', 'Reference']
    line = f.readline().decode('UTF-8')

    for i, h in enumerate(line.replace('\r\n', '').split('\t')):
        
        if h == headers[i]:
            pass
        else:
            print("error")
            return {"validation": False, "error_column": h}

    with open(os.path.join(os.getcwd(), 'datafiles', file_name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    import_data_to_model(file_name, ref_number, ref_link)
    return {'validation': True}
    
def bugs(request):

    if request.method == 'POST':
        form = BugReportingForm(request.POST)
        if form.is_valid():
            now = datetime.now()
            a = BugReporting.objects.create(
                title = form.cleaned_data['title'],
                report_date = now.strftime("%Y-%m-%d"),
                report_time = now.strftime("%H:%M:%S"),
                bug_description = form.cleaned_data['bug_description'],
                user_name  =  form.cleaned_data['user_name'],
            )
            a.save()

            return HttpResponseRedirect('/success')
    else:

        form = BugReportingForm(initial={'title':'','bug_description':'', 'user_name':''})
        
    return render(request, 'DataBase/bug_report_form.html', {'form': form})

def success(request):
    return render(request,  'DataBase/bug_submission_success.html', {})

@staff_member_required
def download_data_report(request):
    return render(request,  'DataBase/uploaded_data_report.html', {})


def import_data_to_model(file_name, ref_num, ref_link):
    f = open(os.path.join(os.getcwd(), 'datafiles', file_name))
    lines = f.readlines()

    count = PeptideSeq.objects.all().count()
    for line in lines[1:]:
        chunks = line.split('\t')
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