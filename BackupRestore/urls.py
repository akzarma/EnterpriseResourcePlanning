from django.conf.urls import url

from BackupRestore import views

app_name = 'BackupRestore'

urlpatterns = [
    # /backup/backup
    url(r'^backup/$', views.backup, name='backup'),
    # /backup/backup/page
    url(r'^backup/(?P<page>[0-9]+)$', views.backup, name='backup'),
    # /backup/restore
    url(r'^restore/', views.restore, name='restore'),
]
