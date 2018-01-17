from django.conf.urls import url

from . import views

app_name = 'Assignment'
urlpatterns = [
    url(r'^add/$', views.add_assignment, name='add_assignment'),
]
