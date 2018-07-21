from django.conf.urls import url, include

from . import views

app_name = 'report'

urlpatterns = [
    url(r'^student', views.student_details, name='student_details'),

    url(r'^faculty', views.faculty_details, name='faculty_details'),

    url(r'^get_excel/$', views.get_excel, name='get_excel'),

    url(r'^get_timetable/$', views.get_timetable, name='get_timetable'),

    url(r'^download_timetable_excel/$', views.download_excel_timetable, name='download_excel_timetable'),

    url(r'^excel_timetable/$', views.excel_timetable, name='excel_timetable'),

    url(r'^excel_room_schedule/$', views.excel_room_schedule, name='excel_room_schedule'),

    url(r'^download_excel_room_schedule/$', views.download_excel_room_schedule, name='download_excel_room_schedule'),

    url(r'^excel_attendance/$', views.excel_attendance, name='excel_attendance'),

    url(r'^download_excel_attendance_subject/$', views.download_excel_attendance_subject,
        name='download_excel_attendance_subject'),

]
