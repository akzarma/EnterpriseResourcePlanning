from django.conf.urls import url

from . import views

app_name = 'Timetable'

urlpatterns = [
    url(r'request/vacant_room$', views.vacant_room, name='vacant_room'),



]
