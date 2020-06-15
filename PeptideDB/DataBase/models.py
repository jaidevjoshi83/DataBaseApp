from django.db import models

# Create your models here.


#class ProteinID(models.Model):
#   ProtID = models.CharField(max_length=30)
#
#   def __str__(self):
#      return "%s" % (self.ProtID)

class PeptideSeq(models.Model):

    Protein_found =models.CharField(max_length=10)
    Recommended_Protein_Name = models.CharField(max_length=200)
    Species = models.CharField(max_length=50)
    Chromosome = models.CharField(max_length=10)
    Accession = models.CharField(max_length=30)
    Input_Sequence = models.CharField(max_length=100)
    P1_Position = models.CharField(max_length=4)
    Cleaving_proteases = models.CharField(max_length=4)

    def __str__(self):
        return "%s %s %s %s %s %s %s %s " % (self.Input_Sequence, self.P1_Position, self.Accession, self.Protein_found, self.Recommended_Protein_Name, self.Species, self.Cleaving_proteases, self.Chromosome )

    class Meta:
        ordering = ['Input_Sequence']




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
