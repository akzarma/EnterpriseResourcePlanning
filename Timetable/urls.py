from django.conf.urls import url

# from Timetable import tasks
from . import views

app_name = 'timetable'

urlpatterns = [
    url(r'enter/$', views.fill_timetable, name='fill_timetable'),
    #
    url(r'^save/$', views.save_timetable, name='save_timetable'),

    url(r'^time_slot/$', views.register_time_slot, name='register_time_slot'),

    # url(r'^to_json/$', views.to_json, name='to_json'),

    url(r'^android_timetable_json/$', views.android_timetable_json, name='android_timetable_json'),

    # url(r'get_excel/$', views.get_excel, name='get_excel'),

    # url(r'^bg_task/$', views.bg_task, name='bg_task')

]
