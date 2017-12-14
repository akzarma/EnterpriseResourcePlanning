from django.conf.urls import url

from Dashboard import views

app_name = "dashboard"

urlpatterns = [
    url(r'^$', views.show_dashboard, name='dashboard'),

    url(r'logout/$', views.logout_user, name="logout"),

    url(r'profile/$', views.view_profile, name="profile"),

    url(r'research/$', views.view_research, name="research"),

    # url(r'^update/', include('Update.urls'))

]
