from django.conf.urls import url

from . import views

app_name = 'update'
urlpatterns = [
    url(r'^$', views.update, name='update'),
    url(r'^role/$', views.update_role, name='update_role'),
    url(r'^exam/status/$', views.update_exam_status, name='update_exam_status'),
    url(r'^subject/status/$', views.update_subject_status, name='update_subject_status'),
]
