from django import forms


class Rand_Frag_From(forms.Form):

    Sequence = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Protein name; Ex. Tropomyosin beta chain '}),required=False)
    Accession = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Uniprot ID; Ex. P02671 '}), required=False)
    #Frag_legnth = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ex.: Y,T,L,K'}))
 
# class Meta:
#     fields = ['Sequence','Accession']

class UploadFileForm(forms.Form):
    file = forms.FileField( )