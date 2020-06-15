from django.contrib import admin
from import_export import resources

from .models import  PeptideSeq

# Register your models here.


class PeptideInfoResource(resources.ModelResource):

    class Meta:
        model = PeptideSeq


#admin.site.register(ProteinID)
admin.site.register(PeptideSeq)