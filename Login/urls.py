from django.conf.urls import url, include

from . import views

app_name = 'login'

urlpatterns = [
    url(r'^$', views.login_user, name='login'),
    url(r'^android/$', views.android_login, name='login_android'),

]
