from django.conf.urls import url

from . import views

app_name = 'registration'

urlpatterns = [
    # /register/student - Register Student
    url(r'^student/$', views.register_student, name='register_student'),

    # /register/faculty - Register Faculty
    url(r'^faculty/$', views.register_faculty, name='register_faculty'),

    url(r'^branch/$', views.register_branch, name='register_branch'),

    url(r'^division/$', views.register_division, name='register_division'),

    # /register/subject - Register Subject
    url(r'^subject/$', views.register_subject, name='register_subject'),

    # /register/year - Register Year Details
    url(r'^year_detail/$', views.register_year_detail, name='register_year_detail'),

    # /register/studentsuccess/ - Register Student
    url(r'^student/success/$', views.success_student, name='success_student'),
    #     # /register/facultysuccess/ - Register Faculty
    url(r'^faculty/success/$', views.success_faculty, name='success_faculty'),

    # /register/view_subjects
    url(r'^view_subjects/$', views.view_subjects, name='view_subjects'),

    url(r'^register_faculty_subject/$', views.register_faculty_subject, name='register_faculty_subject'),

    # /states/
    url(r'^states/India$', views.get_states, name='get_states'),

    url(r'^test/$', views.test, name='test'),

    url(r'^get_division/$', views.get_division, name='get_division'),

    url(r'^get_shift/$', views.get_shift, name='get_shift'),
    # url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'forgot_password/$', views.forgot_password, name='forgot_password'),

    url(r'change_password/$', views.change_password, name='change_password'),

    url(r'student_subject/$', views.student_subject, name='student_subject'),

    url(r'student_subject_division/$', views.student_subject_division, name='student_subject_division'),

    url(r'set_schedule_date/$', views.set_schedule_date, name='set_schedule_date'),

    # url(r'student_subject_registration/$', views.student_subject_registration, name='student_subject_registration'),

    url(r'year/$', views.register_year, name='register_year'),

    url(r'room/$', views.register_room, name='register_room'),

    url(r'^verification/email/(?P<key>[\w]+)/(?P<username>[\w]+)', views.verification_process,
        name="verification_process"),

]
