from django.conf.urls import url

from . import views

app_name = 'update'
urlpatterns = [
    url(r'^$', views.update, name='update'),
    url(r'^role/$', views.update_role, name='update_role'),
]
