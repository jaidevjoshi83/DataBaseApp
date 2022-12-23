from django.shortcuts import render
from .forms import  dabase_form, UploadFileForm, BugReportingForm
from django.contrib.auth import logout
import os
from django.http import HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime
from .models import UploadedData, BugReporting


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
                param = {'acc':accession,'des':description}
                return render(request, 'DataBase/data-table.html', param)
            elif description == '' and accession != '':                
                param = {'acc':accession,'des':'undefined'}
                return render(request, 'DataBase/data-table.html', param)
            elif accession == '' and description != '':
                param = {'acc':'undefined','des':description}
                return render(request, 'DataBase/data-table.html', param)

            elif description == '' and accession == '':
                render(request, 'DataBase/base.html', {'form': form})

    else:
        Fasta = ''
        Acc = ''
        form = dabase_form(initial={'Sequence':Fasta,'Accession':Acc})
        
    logout(request)
    return render(request, 'DataBase/Form.html', {'form': form})

@staff_member_required
def data_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            now = datetime.now()
            dt_string = now.strftime("%d_%m_%Y__%H_%M_%S")
            file_name = "CleavageDB_"+dt_string+'_data_file.csv'

            objs = UploadedData.objects.all()

            a = UploadedData.objects.create(
                datafile_index='DBF'+str(len(UploadedData.objects.all())),
                experiment=form.cleaned_data['experiment_name'],
                data_upload_date=datetime.today(),
                user_name=form.cleaned_data['user'],
                data_description=form.cleaned_data['description'],
                data_file_name=file_name
                )

            print("@@@@@@@@@@@@@", len(objs))

            handle_uploaded_file(request.FILES['file'], file_name)
            a.save()
            return HttpResponseRedirect('/DataUpload/')
    else:
        form = UploadFileForm()
    return render(request, 'DataBase/upload.html', {'form': form})
  
def handle_uploaded_file(f, file_name):

    with open(os.path.join(os.getcwd(), file_name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


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

        print()
        form = BugReportingForm(initial={'title':'','bug_description':'', 'user_name':''})
        
    return render(request, 'DataBase/bug_report_form.html', {'form': form})

def success(request):
    return render(request,  'Database/bug_submission_success.html', {})

def download_data_report(request):
    return render(request,  'Database/bug_submission_success.html', {})
