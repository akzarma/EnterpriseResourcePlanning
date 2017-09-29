from django.conf.urls import url

from . import views

app_name = 'Timetable'

urlpatterns = [
    url(r'enter/$', views.fill_timetable, name='fill_timetable'),

    url(r'get_faculty/$', views.get_faculty, name='get_faculty'),

    # url(r'json/$', views.convert_json, name='json'),

    url(r'^get_faculty/$', views.get_faculty, name='get_faculty'),

    url(r'^to_json/$', views.to_json, name='to_json'),
]
