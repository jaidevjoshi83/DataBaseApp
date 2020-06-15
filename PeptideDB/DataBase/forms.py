from django import forms


class Rand_Frag_From(forms.Form):

    Sequence = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Ex.: AAAAAAGAAGGR'}),required=False)
    Accession = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ex.: Q86U42'}), required=False)
    #Frag_legnth = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ex.: Y,T,L,K'}))
 
class Meta:
    fields = ['Sequence','Accession']



