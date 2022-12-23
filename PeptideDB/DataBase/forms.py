from django import forms


class dabase_form(forms.Form):

    Sequence = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Protein name; Ex. Tropomyosin beta chain '}),required=False)
    Accession = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Uniprot ID; Ex. P02671 '}), required=False)
    #Frag_legnth = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ex.: Y,T,L,K'}))
 
# class Meta:
#     fields = ['Sequence','Accession']

class UploadFileForm(forms.Form):
    experiment_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name of the experiment'}),required=True)
    user = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Who uploaded the data'}),required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description of the data'}), required=True)
    file = forms.FileField( required=True)


class BugReportingForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'a brief title'}),required=True)
    bug_description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description'}), required=True)
    user_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your name (Optional)'}),required=True)