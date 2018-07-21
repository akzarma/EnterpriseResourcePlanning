from django.conf.urls import url, include

from . import views

app_name = 'general'

urlpatterns = [
    url(r'^$', views.general, name='general_code'),

]
