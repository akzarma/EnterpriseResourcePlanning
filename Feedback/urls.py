from django.conf.urls import url

from . import views

app_name = 'Feedback'
urlpatterns = [

    # /dashboard/
    url(r'^self_concept/$', views.self_concept, name='self_concept'),
    url(r'^self_concept/result/$', views.self_concept_result, name='self_concept_result'),
    url(r'^self_concept/pdf/$', views.self_concept_pdf, name='self_concept_pdf'),

]
