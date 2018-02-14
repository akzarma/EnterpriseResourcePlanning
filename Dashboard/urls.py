from django.conf.urls import url

from Dashboard import views

app_name = "dashboard"

urlpatterns = [

    # /dashboard/
    url(r'^$', views.show_dashboard, name='dashboard'),

    # /dashboard/logout
    url(r'logout/$', views.logout_user, name="logout"),

    # /dashboard/profile/
    url(r'profile/$', views.view_profile, name="profile"),

    # /dashboard//research/
    url(r'research/$', views.list_research, name="research"),

    # /dashboard/get_all_excel/
    url(r'get_excel/', views.get_all_excel, name='get_all_excel'),

    # /dashboard/get_excel
    url(r'get_excel/', views.get_excel, name='get_excel')

    # url(r'^update/', include('Update.urls'))

]
