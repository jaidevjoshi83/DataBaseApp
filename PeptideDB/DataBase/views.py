from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import  Rand_Frag_From
from .models import PeptideSeq
# #from .QueryJson import QurJson
from .QueryJson import nti_by_accession
from django.http import JsonResponse
import os
from django.core import serializers
from django.http import HttpResponse
from six.moves.urllib.request import urlopen


import json

# Create your views here.

def HomePage(request):
    return render(request, 'DataBase/base.html', {})

def AboutPage(request):

    peps = PeptideSeq.objects.all()[1:30]
    # print(str(a[3]).split('\t'))

    # peps = []
    # for o in objs:
    #     peps.append(str(o).split('\t'))

    return render(request, 'DataBase/data-table.html', {'peps':peps})

def HelpPage(request):
    return render(request, 'DataBase/help.html', {})

# def DB(request):

#     if request.method == 'POST':
#         form = Rand_Frag_From(request.POST)

#         print(form)

#         if form.is_valid():

#             inputPeptide = form.cleaned_data['Sequence']
#             # accession = form.cleaned_data['Accession']

#             print("OKKKKKK", inputPeptide)

#             Ps = PeptideSeq.objects.all()[3:4]
#             print(Ps)
#             # return render(request, 'DataBase/PepInfo.html', {'Ps': Ps, })
#             return render(request, 'DataBase/data-table.html', {'peps':Ps})
#         else:

#         # Fasta = ''
#         # Acc = ''
#             form = Rand_Frag_From(initial={'Sequence':Fasta})

#         print(form)

#     return render(request, 'DataBase/home.html', {'form': form})


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

def OutData(request):
    return render(request, 'DataBase/OutResults.html', {})

def ProtView(request):
    return render(request, 'DataBase/index.html', {})

def Combined(request):
    return render(request, 'DataBase/index.html', {})

def PepView(request):

    data = {}

    if 'des' in request.GET and 'acc' in request.GET :
        record = PeptideSeq.objects.filter(master_protein_description__contains=request.GET['des'], master_protein_accession__contains=request.GET['acc'])
        qs_json = serializers.serialize('json', record)
        return JsonResponse(qs_json, safe=False)
        # return JsonResponse(nti_by_accession(accession,sequence).to_dict())

    elif  'acc' in request.GET :
        record = PeptideSeq.objects.filter( master_protein_accession__contains=request.GET['acc'])
        qs_json = serializers.serialize('json', record)
        return JsonResponse(qs_json, safe=False)

    elif 'des' in request.GET :
        record = PeptideSeq.objects.filter(master_protein_description__contains=request.GET['des'])
        qs_json = serializers.serialize('json', record)
        return JsonResponse(qs_json, safe=False)
   

def api_nti_peptide(request, accession=None, version=None, sequence=None):
    print(accession)
    print(sequence)
    record = PeptideSeq.objects.filter(master_protein_description__contains=sequence, master_protein_accession__contains=accession)
    qs_json = serializers.serialize('json', record)
    return HttpResponse(qs_json, content_type='json')


    # for i in record:
    #     print(dir(i))

    # print(list(record))
    # return JsonResponse(record, safe = False)
