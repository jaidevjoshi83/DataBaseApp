from django.db import models


class PeptideSeq(models.Model):
       
    db_id = models.CharField(max_length=20,  null=True)
    sequnce = models.CharField(max_length=10,  null=True)
    master_protein_accession = models.CharField(max_length=200,  null=True)
    master_protein_description = models.CharField(max_length=50,  null=True)
    cleavage_site = models.CharField(max_length=10,  null=True)
    annotated_sequence = models.CharField(max_length=30,  null=True)
    abundance = models.CharField(max_length=100  )

    # def __str__(self):
    #     return "%s\t%s\t%s\t%s\t%s\t%s\t%s" % (self.db_id, self.sequnce, self.master_protein_accession, self.master_protein_description, self.cleavage_site, self.annotated_sequence, self.abundance)

    class Meta:
        ordering = ['db_id']


#PeptideSeq.objects.filter(protein_id__ProtID='A0A0B4J1X5')

#ProteinID.objects.filter(peptideseq__sequence='YELTQPPSTAR')
"""
class Peptide(models.Model):

    peptide  = models.CharField(max_length=100)

    def __str__(self):
        return self.peptide

class PeptideInfo(models.Model):

    pep = models.ForeignKey(Peptide, on_delete=models.CASCADE)
    AnnotatedSequence = models.CharField(default= 'No Data',max_length=254)
    CleavageSites = models.CharField(default= 'No Data', max_length=254)
    PreObsCleavageSites = models.CharField(default= 'No Data', max_length=254)
    IsoFormInformation = models.CharField(default= 'No Data',max_length=254)
    AltStartInfo = models.CharField(default= 'No Data',max_length=254)
    KnownProtease = models.CharField(default= 'No Data', max_length=254)
    PeptideSeq = models.CharField(default= 'No Data', max_length=254)
    
    def __str__(self):
        return self.PeptideSeq

"""
