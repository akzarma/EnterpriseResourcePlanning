from django.conf.urls import url

from . import views

app_name = 'update'
urlpatterns = [
    url(r'^student/$', views.update_student, name='update_student'),
    url(r'^role/$', views.update_role, name='update_role'),
]
