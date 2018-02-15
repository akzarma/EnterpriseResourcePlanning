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
    url(r'^download_timetable_excel/$', views.download_excel_timetable, name='download_excel_timtable'),

    # /dashboard/get_all_excel/
    url(r'^excel_timetable/$', views.excel_timetable, name='excel_timetable'),

    # /dashboard/get_excel
    url(r'^get_excel/$', views.get_excel, name='get_excel'),


]
