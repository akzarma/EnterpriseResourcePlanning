from django.conf.urls import url

from . import views

app_name = 'Timetable'

urlpatterns = [
    url(r'enter/$', views.fill_timetable, name='fill_timetable'),

    url(r'^get_faculty/$', views.get_faculty, name='get_faculty'),

    url(r'^get_subject/$', views.get_subject, name='get_subject'),

    url(r'^save/$', views.save_timetable, name='save_timetable'),
]
