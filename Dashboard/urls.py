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

    url(r'^get_timetable/$', views.get_timetable, name='get_timetable'),

    url(r'^toggle_availability/$', views.toggle_availability, name='toggle_availability'),

    url(r'^get_subjects/$', views.get_subjects, name='get_subjects'),

    url(r'^android/get_subjects/$', views.android_get_subjects, name='android_get_subjects'),

    url(r'^set_substitute/(?P<key>[0-9]+)$', views.set_substitute, name='set_substitute'),

    url(r'^android/set_substitute/$', views.android_set_substitute, name='andriod_set_substitute'),

    url(r'^android/toggle_availability$', views.android_toggle_availability, name='android_toggle_availability'),

    url(r'^android/get_date$', views.get_date, name='get_date'),


    url(r'^get_notifications/$', views.get_notifications, name='get_notifications'),

    url(r'^android/get_notifications/$', views.android_get_notifications, name='android_get_notifications'),

    url(r'^show_all_notifications/$', views.show_all_notifications, name='show_all_notifications'),

    url(r'^show_all_notifications/(?P<page>[0-9]+)$', views.show_all_notifications, name='show_all_notifications'),

    url(r'^view_notification/$', views.view_notification, name='view_notification'),



]
