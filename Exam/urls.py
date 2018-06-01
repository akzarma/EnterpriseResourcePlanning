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

]
