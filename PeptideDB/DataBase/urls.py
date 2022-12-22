from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    url(r'HelpPage', views.HelpPage, name='HelpPage'),
    url(r'home', views.DB, name='DB'),
    url(r'PepView', views.PepView, name='PepView'),
    url(r'DataUpload', views.DataUpload, name='DataUpload'),
]