from django.conf.urls import url

from . import views

app_name = 'research'

urlpatterns = [
    # /research/enter - Research Entry
    url(r'^enter/$', views.enter_paper, name='enter_paper'),

]
