from django.http import HttpResponse
from django.shortcuts import render, redirect
import datetime

from shutil import copy

# Create your views here.
from BackupRestore.models import Backup
from EnterpriseResourcePlanning.settings import PROJECT_ROOT, BASE_DIR
from Registration.views import has_role


def backup(request):
    user = request.user
    if not user.is_anonymous:
        # if has_role(user,'faculty'):
        current_time = datetime.datetime.now()
        if request.method == 'GET':
            all_backup = Backup.objects.filter(is_active=True).order_by('version')
            return render(request, 'backup.html', {
                'all_backup': all_backup
            })
        else:
            # print(PROJECT_ROOT)

            previous_latest = Backup.objects.filter(is_latest=True)
            if len(previous_latest) == 1:
                previous_latest = previous_latest[0]
                previous_latest.is_latest = False
                previous_latest.save()
                new_backup_obj = Backup.objects.create(version=previous_latest.version + 0.001, date=current_time)
            elif len(previous_latest) > 1:
                return HttpResponse('There shouldnt be more than 1 latest')
            else:
                new_backup_obj = Backup.objects.create(version=0.001, date=current_time)
                # print(PROJECT_ROOT)
            path = '/BackupRestore/db/'
            # filename = ''
            src = BASE_DIR + '/db.sqlite3'
            new_filename = str(new_backup_obj.version) + '.sqlite3'
            dst = BASE_DIR + path + new_filename
            copy(src=src, dst=dst)

            return redirect('/backup/backup/')


def restore(request):
    user = request.user
    if not user.is_anonymous:
        # if has_role(user,'faculty'):
        current_time = datetime.datetime.now()
        if request.method == 'POST':
            version = request.POST.get('version')
            obj = Backup.objects.get(version=version)
            all_new_version = Backup.objects.filter(version__gt=obj.version)

            filename = version + '.sqlite3'
            path = '/BackupRestore/db/'
            src = BASE_DIR + path + filename
            dst = BASE_DIR + '/db.sqlite3'
            copy(src=src, dst=dst)

            return redirect('/backup/backup/')
