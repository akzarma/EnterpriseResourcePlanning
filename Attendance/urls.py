from django.conf.urls import url

from . import views

app_name = 'attendance'

urlpatterns = [
    url(r'^$', views.index, name="attendance"),
    url(r'^select$', views.select_cat, name="select_cat"),
    url(r'^save$', views.save, name='save')
]
