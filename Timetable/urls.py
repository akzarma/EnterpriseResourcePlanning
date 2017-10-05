from django.conf.urls import url

from . import views

app_name = 'Timetable'

urlpatterns = [
    url(r'enter/$', views.fill_timetable, name='fill_timetable'),

    url(r'^get_faculty/$', views.get_faculty, name='get_faculty'),

    url(r'^save/$', views.save_timetable, name='save_timetable'),

    url(r'^to_json/$', views.to_json, name='to_json'),

    url(r'^get_all_faculty_subject/$', views.get_all_faculty_subject, name='get_all_faculty_subject'),

    url(r'get_timetable/$', views.get_timetable, name='get_timetable'),

    url(r'get_practical_info/$', views.get_practical_info, name='get_practical_info'),

    url(r'^get_instance/$', views.get_instance, name='get_instance'),

    url(r'get_excel/$', views.get_excel, name='get_excel'),

    url(r'get_practical_faculty/$', views.get_practical_faculty, name='get_practical_faculty'),

]
