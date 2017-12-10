from django.conf.urls import url

from . import views

app_name = 'Research'

urlpatterns = [

    url(r'enter/$', views.enter_paper, name='enter_paper'),

]