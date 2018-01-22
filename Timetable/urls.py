from django.conf.urls import url

from . import views

app_name = 'Timetable'

urlpatterns = [
    url(r'enter/$', views.fill_timetable, name='fill_timetable'),

    url(r'^save/$', views.save_timetable, name='save_timetable'),

    url(r'^to_json/$', views.to_json, name='to_json'),

    url(r'get_excel/$', views.get_excel, name='get_excel'),

]
