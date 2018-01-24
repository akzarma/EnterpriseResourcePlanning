from django.conf.urls import url

from . import views

app_name = 'Assignment'
urlpatterns = [
    # url(r'^register/$', views.register_assignment, name='register_assignment'),
    url(r'^start/$', views.start_assignment, name='start_assignment'),
    # url(r'^view/$', views.view_assignment, name='view_assignment'),

]