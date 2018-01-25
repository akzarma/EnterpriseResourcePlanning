from django.conf.urls import url

from . import views

app_name = 'Requests'

urlpatterns = [
    url(r'vacant_room$', views.vacant_room, name='vacant_room'),

]
