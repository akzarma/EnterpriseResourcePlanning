from django.conf.urls import url

from Exam import views

app_name = "exam"
urlpatterns = [

    url(r'^add/$', views.exam_register, name='exam_register'),


]
