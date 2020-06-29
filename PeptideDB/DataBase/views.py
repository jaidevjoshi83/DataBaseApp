from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import  Rand_Frag_From
from .models import PeptideSeq
#from .QueryJson import QurJson
from .QueryJson import nti_by_accession
from django.http import JsonResponse

# Create your views here.

def HomePage(request):
    return render(request, 'DataBase/home.html', {})

def AboutPage(request):
    return render(request, 'DataBase/about.html', {})

def HelpPage(request):
    return render(request, 'DataBase/help.html', {})

def DB(request):

    if request.method == 'POST':
        form = Rand_Frag_From(request.POST)

        if form.is_valid():

            inputPeptide = form.cleaned_data['Sequence']
            accession = form.cleaned_data['Accession']

            if accession =='':
                Ps = PeptideSeq.objects.filter(Input_Sequence=inputPeptide)
                #QurJson(p=inputPeptide)
                return render(request, 'DataBase/PepInfo.html', {'Ps': Ps, })

            if inputPeptide == '':
                #QurJson(a=accession)
                return redirect('http://127.0.0.1:8080/ProtView/?uniprotID='+accession)

            elif accession != '' and inputPeptide != '':
                #QurJson(a=accession, p=inputPeptide)
                return redirect('http://127.0.0.1:8080/ProtView/?Seq='+inputPeptide+'&uniprotID='+accession)
            elif accession == '' and inputPeptide == '':
                return HttpResponseNotFound('<h1>Page not found</h1>')
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

def PepView(request,):

    s = request.GET['s']
    a = request.GET['a']
    
    #QurJson(a=a, p=s)

    return redirect('http://127.0.0.1:8080/ProtView/?Seq='+s+'&uniprotID='+a)

def api_nti_peptide(request, accession=None, version=None, sequence=None):
    print (request) 
    return JsonResponse(nti_by_accession(accession,sequence).to_dict())
