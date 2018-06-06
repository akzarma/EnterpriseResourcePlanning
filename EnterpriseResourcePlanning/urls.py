from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from EnterpriseResourcePlanning import views, settings

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^update/', include('Update.urls')),
    url(r'^register/', include('Registration.urls')),
    url(r'^attendance/', include('Attendance.urls')),
    # url(r'^administrator/', include('administrator.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', include('Login.urls')),
    url(r'^dashboard/', include('Dashboard.urls')),
    url(r'^timetable/', include('Timetable.urls')),
    url(r'^request/', include('Requests.urls')),
    url(r'^report/', include('Report.urls')),
    url(r'^general/', include('General.urls')),
    url(r'^exam/', include('Exam.urls')),
    url(r'^backup/', include('BackupRestore.urls')),
    url(r'^internship/', include('Internship.urls')),
    url(r'^self-concept/', include('SelfConcept.urls'))
    # url(r'^research/', include('Research.urls')),
    # url(r'^update/', include('Update.urls'))

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += staticfiles_urlpatterns()
