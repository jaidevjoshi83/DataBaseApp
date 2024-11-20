from django.db import models
from .utils import  time_stamp

class UploadedData(models.Model):

    upload_type = models.CharField(max_length=50,  null=True) 
    datafile_index = models.CharField(max_length=50,  null=True)
    experiment_name = models.CharField(max_length=100,  null=True)
    data_upload_time = models.TimeField(null=True)
    data_upload_date = models.DateField(null=True)
    user_name = models.CharField(max_length=100,  null=True)
    data_description = models.CharField(max_length=200,  null=True)
    data_file_name = models.CharField(max_length=100,  null=True)
    experiment_type = models.CharField(max_length=20,  null=True)
    reference_link = models.CharField(max_length=300,  null=True)

    class Meta:
        ordering = ['datafile_index']

class PeptideSeq(models.Model):
       
    db_id = models.CharField(max_length=50,  null=True)
    accession = models.CharField(max_length=50,  null=True)
    gene_symbol = models.CharField(max_length=100,  null=True)
    protein_name = models.CharField(max_length=300,  null=True)
    cleavage_site = models.CharField(max_length=200,  null=True)
    peptide_sequence = models.CharField(max_length=300,  null=True)
    annotated_sequence = models.CharField(max_length=300,  null=True)
    cellular_compartment = models.CharField(max_length=300,  null=True)
    species = models.CharField(max_length=100,  null=True)
    database_identified = models.CharField(max_length=100,  null=True)
    description = models.CharField(max_length=300,  null=True)
    reference_link = models.CharField(max_length=300,  null=True)
    data_file_name = models.CharField(max_length=100, null=True)

    # This creates the foreign key relationship with cascade delete
    uploaded_data = models.ForeignKey(UploadedData, on_delete=models.CASCADE, null=False)
    
    class Meta:
        ordering = ['db_id']


class BugReporting(models.Model):
       
    title = models.CharField(max_length=100,  null=True)
    report_date = models.DateField( null=True)
    report_time = models.TimeField( null=True)
    bug_description = models.CharField(max_length=200,  null=True)
    types = models.CharField(max_length=100,  null=True)

    class Meta:
        ordering = ['report_date']

class DataBaseVersion(models.Model):
       
    version = models.CharField(max_length=100,  null=False)
    time_stamp = models.CharField(max_length=100,  null=False)

    class Meta:
        ordering = ['time_stamp']

class File(models.Model):
    existingPath = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)
    eof = models.BooleanField()