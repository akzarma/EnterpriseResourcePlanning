from django.conf.urls import url

from . import views

app_name = 'registration'

urlpatterns = [
    # /register/student - Register Student
    url(r'^student/$', views.register_student, name='register_student'),
    # /register/faculty - Register Faculty
    url(r'^faculty/$', views.register_faculty, name='register_faculty'),
    # /register/subject - Register Subject
    url(r'^subject/$', views.register_subject, name='register_subject'),
    # /register/studentsuccess/ - Register Student
    url(r'^student/success/$', views.success_student, name='success_student'),
    #     # /register/facultysuccess/ - Register Faculty
    url(r'^faculty/success/$', views.success_faculty, name='success_faculty'),

    # /register/view_subjects
    url(r'^view_subjects/$', views.view_subjects, name='view_subjects'),

    url(r'^register_faculty_subject/$' , views.register_faculty_subject , name = 'register_faculty_subject'),
    #     # /register/subjectsuccess/ - Register Subject
    #     url(r'^subject/success/$', views.register_subject, name='register_success'),

    # url(r'^success/$', views.success, name='register_success'),
    # /states/
    url(r'^states/India$', views.get_states, name='get_states'),

    url(r'^test/$', views.test, name='test'),

    url(r'^get_division/$', views.get_division, name='get_division'),

    url(r'^get_shift/$', views.get_shift, name='get_shift'),



]
