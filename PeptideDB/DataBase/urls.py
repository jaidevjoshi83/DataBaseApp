from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    url(r'contact', views.contact, name='contact'),
    url(r'home', views.DB, name='DB'),
    url(r'data_upload', views.data_upload, name='data_upload'),
    url(r'bugs', views.bugs, name='bugs'),
    url(r'success', views.success, name='success'),
]