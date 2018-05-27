from copy import deepcopy

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
import datetime
from django.contrib.auth import authenticate, login

from shutil import copy

# Create your views here.
from BackupRestore.models import Backup
from Dashboard.models import SpecificNotification
from EnterpriseResourcePlanning.settings import PROJECT_ROOT, BASE_DIR, DATABASES, RESTORE_BATCH_SIZE
from Registration.views import has_role
from Timetable.models import Timetable

from Attendance.models import *
from Dashboard.models import *
from Exam.models import *
from Timetable.models import *
from General.models import *
from Registration.models import *
from Attendance.models import FacultyAttendance, StudentAttendance, TotalAttendance
from Dashboard.models import GeneralStudentNotification, SpecificNotification, GeneralFacultyNotification
from Exam.models import ExamMaster, ExamDetail, ExamSubject, Mark, MarksType
from General.models import BranchSubject, Batch, StudentDetail, StudentSubject, YearBranch, Shift, Semester, Schedule, \
    Schedulable, FacultySubject, Division, CollegeYear
from Registration.models import Branch, Student, Subject
from Timetable.models import Timetable, DateTimetable, Room, Time

RESTORE = {Timetable, FacultyAttendance, StudentAttendance, TotalAttendance, GeneralFacultyNotification,
           GeneralStudentNotification, SpecificNotification, ExamDetail, ExamMaster, ExamSubject, Mark, MarksType,
           Batch, BranchSubject, CollegeYear, Division, FacultySubject, Schedulable, Schedule, Semester, Shift,
           StudentDetail, StudentSubject, YearBranch, Branch, Student, Subject, DateTimetable, Room, Time}


def backup(request):
    user = request.user
    if not user.is_anonymous:
        # if has_role(user,'faculty'):
        current_time = datetime.now()
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
                new_backup_obj = Backup.objects.create(version=round(previous_latest.version + 0.001, 3),
                                                       date=current_time)
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


@login_required
def restore(request):
    user = request.user
    if not user.is_anonymous:
        # if has_role(user,'faculty'):
        current_time = datetime.now()
        if request.method == 'POST':
            version = request.POST.get('version')
            obj = Backup.objects.get(version=version)
            all_new_version = Backup.objects.filter(version__gt=obj.version)
            # cpy = deepcopy(all_new_version)
            filename = version + '.sqlite3'
            path = '/BackupRestore/db/'
            src = BASE_DIR + path + filename
            # dst = BASE_DIR + '/db.sqlite3'
            DATABASES['temp'] = {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': src,
            }
            # for each in all_new_version:
            #     each.save(using='temp')
            # copy(src=src, dst=dst)
            # # Backup.objects.bulk_create(cpy,)
            # login(request, user)
            # a = [Timetable, SpecificNotification]

            # for each_table in a:
            batch_migrate()
            DATABASES.pop('temp')
            return redirect('/backup/backup/')
        else:
            return HttpResponse('Not Post')


def batch_migrate():
    for each_table in RESTORE:
        each_table.objects.using('default').all().delete()
        back_objs = each_table.objects.using('temp').all()

        each_table.objects.using('default').bulk_create(back_objs, batch_size=RESTORE_BATCH_SIZE)
