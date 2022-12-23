from django.contrib import admin
from import_export import resources

from .models import  PeptideSeq, UploadedData, BugReporting

# Register your models here.


class PeptideInfoResource(resources.ModelResource):

    class Meta:
        model = PeptideSeq

admin.site.register(PeptideSeq)
admin.site.register(UploadedData)
admin.site.register(BugReporting)