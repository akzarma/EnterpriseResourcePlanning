from django.conf.urls import url

from Attendance import views

app_name = 'attendance'

urlpatterns = [
    # url(r'^$', views.index, name="attendance"),
    url(r'^select$', views.select_cat, name="select_cat"),
    url(r'^save$', views.save, name='save'),
    # url(r'^check$', views.check_attendance, name="check_attendance"),
    url(r'^mark_from_excel$', views.mark_from_excel, name="mark_from_excel"),
    url(r'^android_display_attendance$', views.android_display_attendance, name="android_display_attendance"),
    url(r'^android/fill$', views.android_fill_attendance, name="android_fill_attendance"),
    url(r'^android/instance$', views.android_instance, name="android_instance"),
    url(r'^reload_student_roll/$', views.reload_student_roll, name="reload_student_roll"),

]
