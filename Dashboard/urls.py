from django.conf.urls import url

from Dashboard import views

app_name = "dashboard"
urlpatterns = [

    # /dashboard/
    url(r'^$', views.show_dashboard, name='dashboard'),

    # /dashboard/logout
    url(r'^logout/$', views.logout_user, name="logout"),

    # /dashboard/profile/
    url(r'^profile/$', views.view_profile, name="profile"),

    url(r'^research/$', views.list_research, name="research"),

    url(r'^toggle_availability/$', views.toggle_availability, name='toggle_availability'),

    url(r'^get_subjects/$', views.get_subjects, name='get_subjects'),

    url(r'^android/get_subjects/$', views.android_get_subjects, name='android_get_subjects'),

    url(r'^set_substitute/(?P<key>[0-9]+)$', views.set_substitute, name='set_substitute'),

    url(r'^android/set_substitute/$', views.android_set_substitute, name='andriod_set_substitute'),

    url(r'^android/toggle_availability$', views.android_toggle_availability, name='android_toggle_availability'),

    url(r'^android/get_date$', views.get_date, name='get_date'),

    url(r'^get_notifications/$', views.get_notifications, name='get_notifications'),

    url(r'^android/get_notifications/$', views.android_get_notifications, name='android_get_notifications'),

    url(r'^show_all_notifications/$', views.show_all_notifications, name='show_all_notifications'),

    url(r'^show_all_notifications/(?P<page>[0-9]+)$', views.show_all_notifications, name='show_all_notifications'),

    url(r'^view_notification/$', views.view_notification, name='view_notification'),

    url(r'^read_all_notification/$', views.read_all_notification, name='read_all_notification'),

    url(r'^extra_lecture/$', views.take_extra_lecture, name='take_extra_lecture'),

]
