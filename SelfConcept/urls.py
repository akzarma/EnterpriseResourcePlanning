from django.conf.urls import url

from . import views

app_name = 'SelfConcept'
urlpatterns = [

    # /dashboard/
    url(r'^test/$', views.test, name='test'),

]
