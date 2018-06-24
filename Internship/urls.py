from django.conf.urls import url, include

from . import views

app_name = 'internship'

urlpatterns = [
    url(r'^apply/$', views.apply, name='apply'),
    url(r'^review/$', views.review, name='review'),
    url(r'^status/$', views.status, name='status'),

]
