from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    url(r'HomePage', views.HomePage, name='HomePage'),
    url(r'AboutPage', views.AboutPage, name='AboutPage'),
    url(r'HelpPage', views.HelpPage, name='HelpPage'),
    url(r'DB', views.DB, name='DB'),
    url(r'OutData', views.OutData, name='OutData'),
    url(r'ProtView', views.ProtView, name='ProtView'),
    url(r'PepView', views.PepView, name='PepView'),
    path('api/<int:version>/nti/<str:accession>/<str:sequence>/', views.api_nti_peptide),
    path('api/<int:version>/nti/<str:accession>/', views.api_nti_peptide),

    #url(r'^DATAPLO/(?P<pk>\d+)/$', views.County_Details, name='County_Details'),
]