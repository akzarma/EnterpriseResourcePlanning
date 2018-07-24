from django.conf.urls import url

from Exam import views

app_name = "exam"
urlpatterns = [
    # /exam/add
    url(r'^add/$', views.exam_register, name='exam_register'),
    # /exam/detail
    url(r'^detail/$', views.exam_detail, name='exam_detail'),
    # /exam/get_subjects
    url(r'^get_subjects/$', views.get_subjects, name='get_subjects'),
    # /exam/view_exam
    url(r'^view_exam/$', views.view_exam, name='view_exam'),
    # /exam/manage_exam
    url(r'^manage_exam/$', views.manage_exam, name='manage_exam'),
    # /exam/set_rooms
    url(r'^set_rooms/$', views.set_rooms, name='set_rooms'),
    # /exam/ste_exam_time
    url(r'^set_exam_time/$', views.set_exam_time, name='set_exam_time'),

    url(r'^view_schedule/$', views.view_schedule, name='view_schedule'),
    # /exam/check_availability
    url(r'^check_availability/$', views.check_availability, name='check_availability'),
    # /exam/check_availability/exam_group
    url(r'^check_availability/(?P<still_schedule>[0-9]+)/$', views.check_availability, name='check_availability'),
    # /exam/android/types_of_exam
    url(r'^android/types_of_exam/$', views.android_types_of_exam, name='android_types_of_exam'),
    # /exam/android/exam_subjects
    url(r'^android/exam_subjects/$', views.android_subject_for_exam, name='android_subject_for_exam'),

]
