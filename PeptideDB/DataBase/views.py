from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import  Rand_Frag_From
from .models import PeptideSeq
# #from .QueryJson import QurJson
# from .QueryJson import nti_by_accession
from django.http import JsonResponse
import os

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

            print('OK')

            inputPeptide = form.cleaned_data['Sequence']
            accession = form.cleaned_data['Accession']

            if inputPeptide != '' and accession != '':
                record = PeptideSeq.objects.filter(master_protein_description__contains=inputPeptide, master_protein_accession__contains=accession)
                return render(request, 'DataBase/data-table.html', {'peps':record})
            elif inputPeptide == '':
                record = PeptideSeq.objects.filter( master_protein_accession__contains=accession)
                return render(request, 'DataBase/data-table.html', {'peps':record})
            elif accession == '':
                record = PeptideSeq.objects.filter(master_protein_description__contains=inputPeptide)
                return render(request, 'DataBase/data-table.html', {'peps':record})
            elif inputPeptide == '' and accession == '':
                record = PeptideSeq.objects.filter(master_protein_description__contains=inputPeptide, master_protein_accession__contains=accession)
                render(request, 'DataBase/base.html', {'form': form})

    else:
        Fasta = ''
        Acc = ''
        form = Rand_Frag_From(initial={'Sequence':Fasta,'Accession':Acc})

    
    print("###########")
    return render(request, 'DataBase/Form.html', {'form': form})

def OutData(request):
    return render(request, 'DataBase/OutResults.html', {})

def ProtView(request):
    return render(request, 'DataBase/index.html', {})

def Combined(request):
    return render(request, 'DataBase/index.html', {})

def PepView(request,):

    s = request.GET['s']
    a = request.GET['a']
    
    #QurJson(a=a, p=s)

    return redirect('http://127.0.0.1:8080/ProtView/?Seq='+s+'&uniprotID='+a)

def api_nti_peptide(request, accession=None, version=None, sequence=None):
    print (request) 
    return JsonResponse(nti_by_accession(accession,sequence).to_dict())
