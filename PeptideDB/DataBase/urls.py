from django.urls import path
from . import views

urlpatterns = [
    path(r'contact', views.contact, name='contact'),
    path(r'', views.DB, name='DB'),
    path(r'data_upload', views.data_upload, name='data_upload'),
    path(r'bugs', views.bugs, name='bugs'),
    path(r'success', views.success, name='success'),
    path(r'download_data_report', views.download_data_report, name='download_data_report'),
    path(r'PepView/', views.PepView, name='PepView'),
    path(r'references', views.references, name='references'),
    path(r'data_validation_error', views.data_validation_error, name='data_validation_error'),
    path(r'top_bugs', views.top_bugs, name='top_bugs'),
    path(r'test_view', views.test_view, name='test_view'),
    path(r'admin_activity', views.admin_activity, name='admin_activity'),
    path(r'bug_list', views.bug_list, name='bug_list'),
    path(r'suggestion_list', views.suggestion_list, name='suggestion_list'),
    path(r'logout_view', views.logout_view, name='logout_view'),
]