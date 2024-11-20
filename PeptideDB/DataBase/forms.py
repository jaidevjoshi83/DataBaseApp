from django import forms

class dabase_form(forms.Form):

    Sequence = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Protein name, e.g., Biglycan', 'type':'text'}),required=False)
    Accession = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Uniprot ID, e.g., P21810', 'type':'text'}), required=False)
    Peptide = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Peptide sequence, e.g., DHNKIQA', 'type':'text'}), required=False)

class UploadFileForm(forms.Form):
    experiment_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name of the experiment'}),required=True)
    user = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Who uploaded the data'}),required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description of the data'}), required=True)
    experiment_type = forms.CharField(widget=forms.Select(choices=(('dimethyl', 'Dimethyl'),('itraq', 'iTRAQ'),('tmt', 'TMT'),('label-free', 'Label-free'),('mixed-label', 'Mixed-label'))), required=True)
    reference_number = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name of the experiment'}),required=True)
    reference_link = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name of the experiment'}),required=True)
    file = forms.FileField( required=True)

class BugReportingForm(forms.Form):
    ISSUE_TYPE_CHOICES = [
        ('bug', 'Bug'),
        ('suggestion', 'Suggestion'),
    ]

    issue_type = forms.ChoiceField(
        choices=ISSUE_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )

    subject = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the subject'}),
        required=True,
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter the description', 'id':'contact-form-description'}),
        required=True,
    )