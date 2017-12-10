from django.conf.urls import url

from . import views

app_name = 'attendance'

urlpatterns = [
    url(r'^$', views.index, name="attendance"),
    url(r'^save$', views.save, name='save')
]
