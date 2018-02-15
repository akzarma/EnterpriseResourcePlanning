from django.conf.urls import url

from . import views

app_name = 'login'

urlpatterns = [
    url(r'^$', views.login_user, name='login'),
    url(r'^android/$', views.login_android, name='login_android'),


]
