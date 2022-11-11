from django import forms


class Rand_Frag_From(forms.Form):

    Sequence = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter protein ID; Ex. alpha '}),required=False)
    Accession = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Description; Ex. P02671 '}), required=False)
    #Frag_legnth = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ex.: Y,T,L,K'}))
 
class Meta:
    fields = ['Sequence','Accession']



