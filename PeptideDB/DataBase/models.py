from django.db import models

class PeptideSeq(models.Model):
       
    db_id = models.CharField(max_length=20,  null=True)
    sequence = models.CharField(max_length=10,  null=True)
    master_protein_accession = models.CharField(max_length=200,  null=True)
    master_protein_description = models.CharField(max_length=50,  null=True)
    cleavage_site = models.CharField(max_length=10,  null=True)
    annotated_sequence = models.CharField(max_length=30,  null=True)
    abundance = models.CharField(max_length=100, null=True  )

    class Meta:
        ordering = ['db_id']

class UploadedData(models.Model):
       
    datafile_index = models.CharField(max_length=20,  null=True)
    experiment = models.CharField(max_length=100,  null=True)
    data_upload_date = models.DateField( null=True)
    user_name = models.CharField(max_length=100,  null=True)
    data_description = models.CharField(max_length=200,  null=True)
    data_file_name = models.CharField(max_length=100,  null=True)

    class Meta:
        ordering = ['datafile_index']

class BugReporting(models.Model):
       
    title = models.CharField(max_length=100,  null=True)
    report_date = models.DateField( null=True)
    report_time = models.TimeField( null=True)
    bug_description = models.CharField(max_length=200,  null=True)
    user_name = models.CharField(max_length=100,  null=True)

    class Meta:
        ordering = ['report_date']
