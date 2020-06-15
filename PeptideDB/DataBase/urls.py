from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'HomePage', views.HomePage, name='HomePage'),
    url(r'DB', views.DB, name='DB'),
    url(r'OutData', views.OutData, name='OutData'),
    url(r'ProtView', views.ProtView, name='ProtView'),

    #url(r'^DATAPLO/(?P<pk>\d+)/$', views.County_Details, name='County_Details'),
]