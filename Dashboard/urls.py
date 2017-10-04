from django.conf.urls import url

from Dashboard import views

app_name = "dashboard"

urlpatterns = [
    url(r'^student/', views.test_url, name='student_dashboard'),

    url(r'logout/$', views.logout_user, name="logout"),

    # url(r'^update/', include('Update.urls'))

]