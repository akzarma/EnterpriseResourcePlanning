from django.conf.urls import url
# from django.contrib.auth import views as auth_views

from . import views

app_name = 'login'

urlpatterns = [
    url(r'^android/$', views.login_android, name='login_android'),
    url(r'$', views.login_user, name='login'),
    # url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    # url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     auth_views.password_reset_confirm, name='password_reset_confirm'),
    # url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    # url('^', include('django.contrib.auth.urls')),

]
