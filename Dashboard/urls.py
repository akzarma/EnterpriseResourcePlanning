from django.conf.urls import url

from Dashboard import views

app_name = "dashboard"
urlpatterns = [

    # /dashboard/
    url(r'^$', views.show_dashboard, name='dashboard'),

    # /dashboard/logout
    url(r'^logout/$', views.logout_user, name="logout"),

    # /dashboard/profile/
    url(r'^profile/$', views.view_profile, name="profile"),

    # /dashboard//research/
    url(r'^research/$', views.list_research, name="research"),

    # /dashboard/download_timetable_excel
    url(r'^download_timetable_excel/$', views.download_excel_timetable, name='download_excel_timetable'),

    # /dashboard/excel_timetable/
    url(r'^excel_timetable/$', views.excel_timetable, name='excel_timetable'),

    # /dashboard/excel_room_schedule/
    url(r'^excel_room_schedule/$', views.excel_room_schedule, name='excel_room_schedule'),

    # /dashboard/download_excel_room_schedule
    url(r'^download_excel_room_schedule/$', views.download_excel_room_schedule, name='download_excel_room_schedule'),

    # /dashboard/excel_room_schedule/
    url(r'^excel_attendance/$', views.excel_attendance, name='excel_attendance'),

    # /dashboard/download_excel_room_schedule
    url(r'^download_excel_attendance_subject/$', views.download_excel_attendance_subject, name='download_excel_attendance_subject'),



    # /dashboard/get_excel
    url(r'^get_excel/$', views.get_excel, name='get_excel'),

]
