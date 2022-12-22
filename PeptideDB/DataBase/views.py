from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import  Rand_Frag_From
from .models import PeptideSeq
import os
# #from .QueryJson import QurJson

from django.http import JsonResponse
import os
from django.core import serializers
from django.http import HttpResponse
from six.moves.urllib.request import urlopen


from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from django.core.files import uploadedfile
from django.contrib.admin.views.decorators import staff_member_required


import json

# Create your views here.


def HelpPage(request):
    return render(request, 'DataBase/help.html', {})

def DB(request):

    if request.method == 'POST':
        form = Rand_Frag_From(request.POST)

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
        form = Rand_Frag_From(initial={'Sequence':Fasta,'Accession':Acc})

    return render(request, 'DataBase/Form.html', {'form': form})


def PepView(request):

    data = {}

    if 'des' in request.GET and 'acc' in request.GET :
        record = PeptideSeq.objects.filter(master_protein_description__contains=request.GET['des'], master_protein_accession__contains=request.GET['acc'])
        qs_json = serializers.serialize('json', record)
        return JsonResponse(qs_json, safe=False)

    elif  'acc' in request.GET :
        record = PeptideSeq.objects.filter( master_protein_accession__contains=request.GET['acc'])
        qs_json = serializers.serialize('json', record)
        return JsonResponse(qs_json, safe=False)

    elif 'des' in request.GET :
        record = PeptideSeq.objects.filter(master_protein_description__contains=request.GET['des'])
        qs_json = serializers.serialize('json', record)
        return JsonResponse(qs_json, safe=False)

@staff_member_required
def DataUpload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
       
        if form.is_valid():
            print(request.FILES['file'])
            print(uploadedfile)
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/DataUpload/')
    else:
        form = UploadFileForm()
    return render(request, 'DataBase/upload.html', {'form': form})
  
def handle_uploaded_file(f):
    with open(os.getcwd()+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
