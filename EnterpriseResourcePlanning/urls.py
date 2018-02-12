from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^$', include('Login.urls')),
    url(r'^update/', include('Update.urls')),
    url(r'^register/', include('Registration.urls')),
    url(r'^attendance/', include('Attendance.urls')),
    # url(r'^administrator/', include('administrator.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', include('Login.urls')),
    url(r'^dashboard/', include('Dashboard.urls')),
    url(r'^timetable/', include('Timetable.urls')),
    url(r'^request/', include('Requests.urls')),
    url(r'^research/', include('Research.urls')),
    # url(r'^update/', include('Update.urls'))

]
