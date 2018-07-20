import json, copy
from collections import OrderedDict
from itertools import chain

import xlsxwriter
from django import urls
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt

from Attendance.models import StudentAttendance
from Dashboard.models import SpecificNotification, GeneralStudentNotification, GeneralFacultyNotification
from EnterpriseResourcePlanning.settings import NOTIFICATION_LONG_LIMIT, NOTIFICATION_SMALL_LIMIT
from General.models import Batch, StudentDetail, Division, CollegeYear, FacultySubject, BranchSubject, YearBranch, \
    ElectiveDivision, Semester, YearSemester, Shift
from General.views import notify_users
from Registration.forms import StudentForm, FacultyForm
from Registration.models import Student, Branch, Faculty, ElectiveSubject, Subject
import datetime

# Student dashboard
from Registration.views import has_role
from Research.models import Paper
from Timetable.models import Timetable, DateTimetable, Time, Room
from Update.forms import StudentUpdateForm, FacultyUpdateForm
from Roles.models import RoleMaster, RoleManager


# def student(request):
#     user = request.user
#     # If user exists in session (i.e. logged in)
#     if not user.is_anonymous:
#         student_obj = user.student
#         form = StudentForm(instance=student_obj)
#         return render(request, 'dashboard.html', {
#             'form': form,
#             'first_name': user.first_name,
#             'last_name': user.last_name,
#
#         })
#     else:
#         return HttpResponseRedirect('/login/')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def show_dashboard(request):
    class_active = "dashboard"
    user = request.user
    # If user exists in session (i.e. logged in)
    if not user.is_anonymous:
        is_faculty = has_role(user, 'faculty')
        is_student = has_role(user, 'student')
        if is_student:
            student = user.student
            attendance = {}
            #     attended = 0
            #    total = 0
            #     total_attendance = student.totalattendance_set.all()

            #      for each in total_attendance:
            #         total += each.total_lectures
            #         attended += each.attended_lectures
            #          if each.total_lectures is not 0:
            #              subject_attendance = round(100 * each.attended_lectures / each.total_lectures, 2)
            #          else:
            #              subject_attendance = 0
            #           attendance[each.subject.short_form] = {
            #                'total': each.total_lectures,
            #                 'attended': each.attended_lectures,
            #                  'attendance': subject_attendance,
            #               }
            #            total_percent = round(100 * attended / total, 2) if total is not 0 else 0

            college_extra_detail = StudentDetail.objects.get(student=student, is_active=True).batch.division
            if request.method == "GET":
                timetable = sorted(
                    DateTimetable.objects.filter(date=datetime.date.today(), original__division=college_extra_detail,
                                                 is_active=True),
                    key=lambda x: (x.date, x.original.time.starting_time))

                return render(request, 'dashboard_student.html', {
                    'timetable': timetable,
                    'selected_date': datetime.date.today().strftime('%d-%m-%Y'),
                })
            else:
                if 'GO' in request.POST:
                    selected_date = datetime.datetime.strptime(request.POST.get('selected_date'), '%d-%m-%Y').date()
                    timetable = sorted(
                        DateTimetable.objects.filter(date=selected_date,
                                                     original__division=college_extra_detail, is_active=True),
                        key=lambda x: (x.date, x.original.time.starting_time))

                    return render(request, 'dashboard_student.html', {
                        'timetable': timetable,
                        'selected_date': selected_date.strftime('%d-%m-%Y'),
                    })

                elif request.POST.__contains__('previous') or request.POST.__contains__('next'):
                    selected_date = datetime.datetime.strptime(request.POST.get('selected_date'), '%d-%m-%Y').date()
                    if request.POST.get('previous'):
                        selected_date = selected_date + datetime.timedelta(-1)

                    if request.POST.get('next'):
                        selected_date = selected_date + datetime.timedelta(1)

                    timetable = sorted(
                        DateTimetable.objects.filter(date=selected_date,
                                                     original__division=college_extra_detail, is_active=True),
                        key=lambda x: (x.date, x.original.time.starting_time))

                    return render(request, 'dashboard_student.html', {
                        'timetable': timetable,
                        'selected_date': selected_date.strftime('%d-%m-%Y'),
                    })

        elif is_faculty:
            faculty = user.faculty

            if request.method == "GET":
                timetable = sorted(
                    DateTimetable.objects.filter(date=datetime.date.today(), original__faculty=faculty, is_active=True),
                    key=lambda x: (x.date, x.original.time.starting_time))
                return render(request, 'dashboard_faculty.html', {
                    'class_active': class_active,
                    'timetable': timetable,
                    'selected_date': datetime.date.today().strftime('%d-%m-%Y'),
                })

            else:
                if 'GO' in request.POST:
                    selected_date = datetime.datetime.strptime(request.POST.get('selected_date'), '%d-%m-%Y').date()
                    timetable = sorted(
                        DateTimetable.objects.filter(Q(date=selected_date), Q(is_active=True),
                                                     Q(original__faculty=faculty) | Q(substitute__faculty=faculty)),
                        key=lambda x: (x.date, x.original.time.starting_time))

                    return render(request, 'dashboard_faculty.html', {
                        'class_active': class_active,
                        'timetable': timetable,
                        'selected_date': selected_date.strftime('%d-%m-%Y'),
                    })

                elif request.POST.__contains__('previous') or request.POST.__contains__('next'):
                    selected_date = datetime.datetime.strptime(request.POST.get('selected_date'), '%d-%m-%Y').date()
                    if request.POST.get('previous'):
                        selected_date = selected_date + datetime.timedelta(-1)

                    if request.POST.get('next'):
                        selected_date = selected_date + datetime.timedelta(1)

                    timetable = sorted(
                        DateTimetable.objects.filter(Q(date=selected_date), Q(is_active=True),
                                                     Q(original__faculty=faculty) | Q(substitute__faculty=faculty)),
                        key=lambda x: (x.date, x.original.time.starting_time))

                    return render(request, 'dashboard_faculty.html', {
                        'class_active': class_active,
                        'timetable': timetable,
                        'selected_date': selected_date.strftime('%d-%m-%Y'),
                    })

                elif 'date_timetable' in request.POST:
                    selected_date = datetime.datetime.strptime(request.POST.get('selected_date'), '%d-%m-%Y').date()
                    timetable = sorted(
                        DateTimetable.objects.filter(Q(date=selected_date), Q(is_active=True),
                                                     Q(original__faculty=faculty) | Q(substitute__faculty=faculty)),
                        key=lambda x: (x.date, x.original.time.starting_time))

                    selected_class_obj = DateTimetable.objects.get(pk=request.POST.get('date_timetable'),
                                                                   is_active=True)

                    if selected_class_obj.original.is_practical:
                        attendance = StudentAttendance.objects.filter(
                            student__studentdetail__batch=selected_class_obj.original.batch,
                            student__studentdetail__is_active=True,
                            timetable=selected_class_obj)

                        present_roll = sorted(
                            [StudentDetail.objects.get(student=each.student, is_active=True).roll_number for each in
                             attendance if
                             each.attended is True])

                        all_students = StudentDetail.objects.filter(
                            batch=selected_class_obj.original.batch, is_active=True).values_list('student', flat=True)
                        all_students_roll = sorted(
                            [StudentDetail.objects.get(student=each, is_active=True).roll_number for
                             each in all_students])

                    else:
                        attendance = StudentAttendance.objects.filter(timetable=selected_class_obj)
                        present_roll = sorted(
                            [StudentDetail.objects.get(student=each.student, is_active=True).roll_number
                             for each in attendance if each.attended is True])

                        all_students = StudentDetail.objects.filter(
                            batch__division=selected_class_obj.original.division, is_active=True) \
                            .values_list('student', flat=True)
                        all_students_roll = sorted(
                            [StudentDetail.objects.get(student=each, is_active=True).roll_number for
                             each in all_students])

                    if attendance:
                        att = 1

                    else:
                        att = 0

                    return render(request, 'dashboard_faculty.html', {
                        'class_active': class_active,
                        'timetable': timetable,
                        'selected_date': selected_date.strftime('%d-%m-%Y'),
                        'att': att,
                        'selected_timetable': selected_class_obj,
                        'all_students_roll': all_students_roll,
                        'present_roll': present_roll,
                    })

        else:
            logout_user(request)  # Show 404 Page
            return redirect('/login/')
    else:
        return redirect('/login/')


def view_profile(request):
    user = request.user
    if not user.is_anonymous:
        is_faculty = RoleManager.objects.filter(user=user, role__role='faculty')
        is_student = RoleManager.objects.filter(user=user, role__role='student')
        if request.method == 'POST':
            if is_student:
                form = StudentUpdateForm(request.POST, request.FILES, instance=user.student)
                if form.is_valid():
                    student_obj = form.save(commit=False)
                    student_obj.user = user
                    student_obj.save()
                    return HttpResponseRedirect('/dashboard/')
                else:
                    return render(request, 'profile_student.html', {
                        'form': form,
                    })

            elif is_faculty:
                form = FacultyUpdateForm(request.POST, request.FILES, instance=user.faculty)
                if form.is_valid():
                    faculty_obj = form.save(commit=False)
                    faculty_obj.user = user
                    faculty_obj.save()
                    return HttpResponseRedirect('/dashboard/')
                else:
                    return render(request, 'profile_faculty.html', {
                        'form': form,
                    })

        else:
            if is_faculty:
                obj = user.faculty
                form = FacultyUpdateForm(instance=obj)
                return render(request, 'profile_faculty.html', {
                    'form': form,
                })

            elif is_student:
                obj = user.student
                form = StudentUpdateForm(instance=obj)
                return render(request, 'profile_student.html', {
                    'form': form,
                })

            else:
                return HttpResponse("User has no role")


    else:
        return HttpResponseRedirect('/login/')


def list_research(request):
    user = request.user
    all_papers = Paper.objects.filter(faculty=user.faculty)
    return render(request, 'list_research.html', {'all_papers': all_papers})


def toggle_availability(request):
    selected_timetable = DateTimetable.objects.get(pk=request.POST.get('selected_timetable'))
    timetable_obj = selected_timetable.original
    send_notification = False
    student_message = 'Lecture on ' + selected_timetable.date.__str__() + ', ' + timetable_obj.time.__str__()

    if selected_timetable.not_available is True:
        if selected_timetable.is_substituted is False:
            selected_timetable.not_available = False
            student_message += ' has been taken by ' + timetable_obj.faculty.initials + '.'
        else:
            if request.user.faculty == selected_timetable.substitute.faculty:
                selected_timetable.is_substituted = False
                send_notification = True
                student_message += 'has been cancelled.'
            else:
                return HttpResponse(
                    'Sorry, ' + selected_timetable.substitute.faculty.initials + ' has already taken your lecture!')
    else:
        selected_timetable.not_available = True
        send_notification = True
        student_message += ' has been cancelled'

    if send_notification:
        selected_timetable.save()
        # date = timetable_obj.date
        time = timetable_obj.time

        division = timetable_obj.division

        all_faculty_that_div = list(FacultySubject.objects.filter(division=division,
                                                                  subject__is_practical=timetable_obj.is_practical).values_list(
            'faculty', flat=True))

        all_tt_obj_at_that_time = DateTimetable.objects.filter(date=selected_timetable.date, original__time=time)

        all_faculty_at_that_time = []

        for each_tt in all_tt_obj_at_that_time:
            # Add substitute instead of original
            if each_tt.is_substituted:
                all_faculty_at_that_time.append(each_tt.substitute.faculty.user.username)
            else:
                if not each_tt.not_available:
                    all_faculty_at_that_time.append(each_tt.original.faculty.user.username)

        free_faculty = (
                set(all_faculty_that_div) - (
            set(list(all_faculty_at_that_time) + [timetable_obj.faculty.user.username])))
        # free_faculty
        free_faculty = [Faculty.objects.get(pk=each) for each in free_faculty]
        print('Free', free_faculty)

        message = 'There is a free lecture available right now for ' + division.year_branch.year.year + ' ' + division.division + ' on ' \
                  + str(selected_timetable.date) + ' ' + time.__str__()

        notification_type = 'specific'

        heading = 'Empty Lecture Slot'

        users_obj = [each_faculty.user for each_faculty in free_faculty]
        action = urls.reverse('dashboard:set_substitute', args=[selected_timetable.pk])
        type = "Decision"
        # For specific faculty
        notify_users(notification_type=notification_type, message=message, heading=heading, users_obj=users_obj,
                     type=type, action=action)

        # For generic students
        # division
        notify_users(notification_type='general', user_type='Student', message=student_message,
                     heading='Change in a lecture schedule', users_obj=[], division=[division], )

    return HttpResponse('success')


def get_notifications(request):
    user = request.user
    if not user.is_anonymous:
        if request.is_ajax():
            date = datetime.date.today().strftime('%Y-%m-%d')
            notification_objs = SpecificNotification.objects.filter(user=user, is_active=True, has_read=False)[
                                :NOTIFICATION_SMALL_LIMIT]

            data = {'today': date}

            is_faculty = has_role(user, 'faculty')
            is_student = has_role(user, 'student')

            if is_student:
                student_obj = user.student
                student_detail_obj = StudentDetail.objects.get(student=student_obj, is_active=True)
                division_obj = student_detail_obj.batch.division
                general_notification_obj = GeneralStudentNotification.objects.filter(division=division_obj,
                                                                                     is_active=True)[
                                           :NOTIFICATION_SMALL_LIMIT]

            elif is_faculty:
                faculty_obj = user.faculty
                faculty_sub_obj = list(FacultySubject.objects.filter(faculty=faculty_obj, is_active=True))
                branch_obj = list(
                    BranchSubject.objects.filter(subject_id__in=[each.subject_id for each in faculty_sub_obj],
                                                 is_active=True))
                branch_obj = list(set([each.year_branch.branch for each in branch_obj]))
                general_notification_obj = GeneralFacultyNotification.objects.filter(branch__in=branch_obj,
                                                                                     is_active=True)[
                                           :NOTIFICATION_SMALL_LIMIT]

                num_general_notification = len(general_notification_obj)
            all_notifications = list(notification_objs) + list(general_notification_obj)
            final_notifications = sorted(all_notifications, key=lambda x: x.datetime)[:NOTIFICATION_SMALL_LIMIT]

            for each in range(len(final_notifications)):
                if not each in data:
                    data[each] = serializers.serialize('json', [final_notifications[each], ], fields=(
                        'heading', 'datetime', 'type', 'notification', 'has_read', 'action', 'priority'))
                    # if final_notifications[each] in general_notification_obj:
                    #     data[each]['is_general'] = 'true'
                    # else:
                    #     data[each]['is_general'] = 'false'

                    struct = json.loads(data[each])
                    struct[0]['is_general'] = final_notifications[each] in general_notification_obj
                    data[each] = json.dumps(struct[0])

            return HttpResponse(json.dumps(data))

        else:
            return HttpResponse("Not ajax.Should be ajax")
    else:
        return redirect('/login/')


def show_all_notifications(request, page=1):
    user = request.user
    if not user.is_anonymous:
        is_faculty = RoleManager.objects.filter(user=user, role__role='faculty')
        is_student = RoleManager.objects.filter(user=user, role__role='student')
        notification_objs = SpecificNotification.objects.filter(user=user)[
                            (int(page) - 1) * NOTIFICATION_LONG_LIMIT:(int(
                                page) - 1) * NOTIFICATION_LONG_LIMIT + NOTIFICATION_LONG_LIMIT]
        general_notification_student = []
        all_notifications = []
        if is_student:
            student_obj = user.student
            student_detail_obj = StudentDetail.objects.get(student=student_obj, is_active=True)
            division_obj = student_detail_obj.batch.division
            general_notification_student = GeneralStudentNotification.objects.filter(division=division_obj,
                                                                                     is_active=True)[
                                           :NOTIFICATION_LONG_LIMIT]
            all_notifications = list(notification_objs) + list(general_notification_student)

        elif is_faculty:
            faculty_obj = user.faculty
            faculty_sub_obj = list(FacultySubject.objects.filter(faculty=faculty_obj, is_active=True))
            branch_obj = list(
                BranchSubject.objects.filter(subject_id__in=[each.subject_id for each in faculty_sub_obj],
                                             is_active=True))
            branch_obj = list(set([each.year_branch.branch for each in branch_obj]))
            general_notification_faculty = GeneralFacultyNotification.objects.filter(branch__in=branch_obj,
                                                                                     is_active=True)[
                                           :NOTIFICATION_LONG_LIMIT]
            all_notifications = list(notification_objs) + list(general_notification_faculty)

        final_notifications = sorted(all_notifications, key=lambda x: x.datetime, reverse=True)[
                              :NOTIFICATION_LONG_LIMIT]

        notification_model = {}
        for obj in final_notifications:
            if obj in general_notification_student:
                notification_model[obj.pk] = 'GeneralStudent'
            elif obj in general_notification_faculty:
                notification_model[obj.pk] = 'GeneralFaculty'
            else:
                notification_model[obj.pk] = 'SpecificNotification'

        pages = len(final_notifications)
        pages = pages // 50
        pages += 1 if pages % 50 is not 0 else 0
        if pages == 0:
            pages = 1

        return render(request, 'all_notifications.html', {
            'notifications': final_notifications,
            'pages': range(1, pages + 1),
            'current_page': int(page),
            'notification_model': json.dumps(notification_model)
        })
    return redirect('/login/')


def view_notification(request):
    model = request.POST.get('model')
    if model == 'GeneralStudent':
        notification = GeneralStudentNotification.objects.get(pk=int(request.POST.get('pk')))

    elif model == 'GeneralFaculty':
        notification = GeneralFacultyNotification.objects.get(pk=int(request.POST.get('pk')))
    else:
        notification = SpecificNotification.objects.get(user=request.user, pk=int(request.POST.get('pk')))
        notification.has_read = True
        notification.save()

    data = serializers.serialize('json', [notification, ])
    struct = json.loads(data)
    data = json.dumps(struct[0])
    return HttpResponse(data)


def set_substitute(request, key):
    user = request.user
    if not user.is_anonymous:
        is_faculty = RoleManager.objects.filter(user=user, role__role='faculty')
        if is_faculty:
            if request.method == "POST":
                selected_timetable = DateTimetable.objects.get(pk=int(key))
                if selected_timetable.not_available is True:
                    if selected_timetable.is_substituted is True:
                        return HttpResponse("Sorry, this lecture has already been taken by someone else.")

                    selected_timetable.is_substituted = True
                    subject = BranchSubject.objects.get(
                        year_branch=selected_timetable.original.branch_subject.year_branch,
                        subject__short_form=request.POST.get('subject'))

                    substitute_tt = Timetable.objects.create(room=selected_timetable.original.room,
                                                             time=selected_timetable.original.time,
                                                             day=selected_timetable.original.day,
                                                             division=selected_timetable.original.division,
                                                             branch_subject=subject, faculty=user.faculty,
                                                             is_practical=selected_timetable.original.is_practical,
                                                             batch=selected_timetable.original.batch)

                    selected_timetable.substitute = substitute_tt
                    selected_timetable.save()
                    return HttpResponse("success")

                else:
                    return HttpResponse("Sorry, this lecture is not available to be taken! ")
            return HttpResponse("You don't have enough priviledges to use this function")
    return redirect('/login/')


def get_subjects(request):
    user = request.user
    if not user.is_anonymous:
        is_faculty = RoleManager.objects.filter(user=user, role__role='faculty')
        if is_faculty:
            if request.method == "POST":
                selected_timetable = DateTimetable.objects.get(pk=int(request.POST.get('id')))

                original_timetable = selected_timetable.original

                subjects = FacultySubject.objects.filter(faculty=user.faculty, division=original_timetable.division,
                                                         subject__is_practical=original_timetable.is_practical).values_list(
                    'subject__short_form', flat=True)

            return HttpResponse(json.dumps(list(subjects)))
        return HttpResponse('Not Priviledged Enough to use this function!')
    return HttpResponseRedirect('/login/')


@csrf_exempt
def android_get_notifications(request):
    if request.method == "POST":
        user = User.objects.get(username=request.POST.get('username'))
        print(request.POST.get('pk_specific'))
        pk_specific = int(request.POST.get('pk_specific'))
        pk_general = int(request.POST.get('pk_general'))
        specific_notification_objs = SpecificNotification.objects.filter(user=user, is_active=True, pk__gt=pk_specific)
        general_notification_objs = []
        if has_role(user, 'faculty'):
            faculty_obj = user.faculty
            faculty_sub_obj = list(FacultySubject.objects.filter(faculty=faculty_obj, is_active=True))
            branch_obj = list(
                BranchSubject.objects.filter(subject_id__in=[each.subject_id for each in faculty_sub_obj],
                                             is_active=True))
            branch_obj = list(set([each.year_branch.branch for each in branch_obj]))
            general_notification_objs = GeneralFacultyNotification.objects.filter(branch__in=branch_obj,
                                                                                  is_active=True, pk__gt=pk_general)[
                                        :NOTIFICATION_LONG_LIMIT]
        elif has_role(user, 'student'):
            student_obj = user.student
            student_detail_obj = StudentDetail.objects.get(student=student_obj, is_active=True)
            division_obj = student_detail_obj.batch.division
            general_notification_objs = GeneralStudentNotification.objects.filter(division=division_obj,
                                                                                  is_active=True, pk__gt=pk_general)[
                                        :NOTIFICATION_LONG_LIMIT]
        # print(pk)
        data1 = {}

        for each in range(len(specific_notification_objs)):
            if not each in data1:
                data1[each] = serializers.serialize('json', [specific_notification_objs[each], ], fields=(
                    'heading', 'datetime', 'type', 'notification', 'has_read', 'action', 'priority'))
                data1[each] = json.loads(data1[each])[0]
                # data[each] = json.dumps(struct[0])
        answer = {}
        # answer['timeline'] = {'specific': {},
        #                       'general': {}
        #                       }
        answer['specific'] = data1
        data2 = {}
        for each in range(len(general_notification_objs)):
            if not each in data2:
                data2[each] = serializers.serialize('json', [general_notification_objs[each], ], fields=(
                    'heading', 'datetime', 'type', 'notification', 'action', 'priority'))
                data2[each] = json.loads(data2[each])[0]
                # data[each] = json.dumps(struct[0])
        answer['general'] = data2

        return JsonResponse(answer)
    else:
        return JsonResponse({'error': 'Not a post request'})


@csrf_exempt
def get_date(request):
    date = timezone.now().__str__()
    return HttpResponse(date)


@csrf_exempt
def android_set_substitute(request):
    user = User.objects.get(username=request.POST.get('username'))
    selected_timetable = DateTimetable.objects.get(pk=int(request.POST.get('pk')))
    if selected_timetable.not_available is True:
        if selected_timetable.is_substituted is True:
            return HttpResponse("Sorry, this lecture has already been taken.")

        selected_timetable.is_substituted = True
        subject = BranchSubject.objects.get(
            year_branch=selected_timetable.original.branch_subject.year_branch,
            subject__short_form=request.POST.get('choice'))

        substitute_tt = Timetable.objects.create(room=selected_timetable.original.room,
                                                 time=selected_timetable.original.time,
                                                 day=selected_timetable.original.day,
                                                 division=selected_timetable.original.division,
                                                 branch_subject=subject, faculty=user.faculty,
                                                 is_practical=selected_timetable.original.is_practical,
                                                 batch=selected_timetable.original.batch)

        selected_timetable.substitute = substitute_tt
        selected_timetable.save()
        return HttpResponse("success")

    else:
        return HttpResponse("Sorry, this lecture is not available to be taken! ")


@csrf_exempt
def android_get_subjects(request):
    user = User.objects.get(username=request.POST.get('username'))
    selected_timetable = DateTimetable.objects.get(pk=int(request.POST.get('pk')))
    original_timetable = selected_timetable.original

    subjects = FacultySubject.objects.filter(faculty=user.faculty, division=original_timetable.division,
                                             subject__is_practical=original_timetable.is_practical).values_list(
        'subject__short_form', flat=True)

    return HttpResponse(json.dumps(list(subjects)))


@csrf_exempt
def android_toggle_availability(request):
    return HttpResponse("Yeah!")


def read_all_notification(request):
    pk = json.loads(request.POST.get('pk'))
    for each in pk:
        notification = SpecificNotification.objects.get(pk=int(each))
        notification.has_read = True
        notification.save()
    return HttpResponse("Done")


def take_extra_lecture(request):
    user = request.user
    if not user.is_anonymous:
        if has_role(user, 'faculty'):
            faculty = user.faculty
            data = {}
            year_branch = [i.division.year_branch for i in
                           FacultySubject.objects.filter(faculty=faculty, subject__is_elective_group=False)]

            for each in year_branch:
                if not each.branch.branch in data:
                    data[each.branch.branch] = {}
                if not each.year.year in data[each.branch.branch]:
                    data[each.branch.branch][each.year.year] = []

                data[each.branch.branch][each.year.year] = list(Division.objects.filter(year_branch=each,
                                                                                        is_active=True).values_list(
                    'division',
                    flat=True).distinct())

            for i in FacultySubject.objects.filter(faculty=faculty, subject__is_elective_group=True):
                if i.elective_division is not None:
                    elective_year_branch = BranchSubject.objects.get(subject=i.subject, is_active=True).year_branch

                    if not elective_year_branch.branch.branch in data:
                        data[elective_year_branch.branch.branch] = {}
                    if not elective_year_branch.year.year in data[elective_year_branch.branch.branch]:
                        data[elective_year_branch.branch.branch][elective_year_branch.year.year] = []

                    data[elective_year_branch.branch.branch][elective_year_branch.year.year] += [
                        i.subject.short_form + "--" + i.elective_division.elective_subject.short_form + "--" + str(
                            i.elective_division.division)]

            if request.method == "GET":
                return render(request, 'extra_lecture.html', {
                    'data': data
                })

            else:
                if request.POST.__contains__('date_form'):
                    branch = request.POST.get('branch')
                    year = request.POST.get('year')
                    division = request.POST.get('division')
                    selected_date = parse_date(request.POST.get('selected_date'))
                    year_branch_object = YearBranch.objects.get(year__year=year, branch__branch=branch)

                    all_timetable = list(DateTimetable.objects.filter(date=selected_date))

                    all_rooms_theory = set(
                        Room.objects.filter(branch=year_branch_object.branch, lab=False).values_list('room_number',
                                                                                                     flat=True))

                    all_rooms_practical = set(
                        Room.objects.filter(branch=year_branch_object.branch, lab=True).values_list('room_number',
                                                                                                    flat=True))

                    room_dict = {}

                    for each_tt in all_timetable:
                        if each_tt.not_available:
                            if each_tt.is_substituted:

                                if each_tt.substitute.time.__str__() in room_dict:
                                    if each_tt.substitute.room.lab:
                                        room_dict[each_tt.substitute.time.__str__()]['practical'].append(
                                            each_tt.substitute.room.room_number)
                                    else:
                                        room_dict[each_tt.substitute.time.__str__()]['theory'].append(
                                            each_tt.substitute.room.room_number)
                                else:
                                    room_dict[each_tt.substitute.time.__str__()] = {
                                        'theory': [],
                                        'practical': []
                                    }
                                    if each_tt.substitute.room.lab:
                                        room_dict[each_tt.substitute.time.__str__()]['practical'] = [
                                            each_tt.substitute.room.room_number]
                                    else:
                                        room_dict[each_tt.substitute.time.__str__()]['theory'] = [
                                            each_tt.substitute.room.room_number]
                                # used_rooms.append(each_tt.substitute.room.room_number)
                        else:
                            if each_tt.original.time.__str__() in room_dict:
                                if each_tt.original.room.lab:
                                    room_dict[each_tt.original.time.__str__()]['practical'].append(
                                        each_tt.original.room.room_number)
                                else:
                                    room_dict[each_tt.original.time.__str__()]['theory'].append(
                                        each_tt.original.room.room_number)
                            else:
                                room_dict[each_tt.original.time.__str__()] = {
                                    'theory': [],
                                    'practical': []
                                }
                                if each_tt.original.room.lab:
                                    room_dict[each_tt.original.time.__str__()]['practical'] = [
                                        each_tt.original.room.room_number]
                                else:
                                    room_dict[each_tt.original.time.__str__()]['theory'] = [
                                        each_tt.original.room.room_number]

                    for slot, rooms in room_dict.items():
                        room_dict[slot]['theory'] = list(all_rooms_theory.difference(set(room_dict[slot]['theory'])))
                        room_dict[slot]['practical'] = list(
                            all_rooms_practical.difference(set(room_dict[slot]['practical'])))

                    if '--' not in division:
                        division_object = Division.objects.get(year_branch=year_branch_object,
                                                               division=division,
                                                               is_active=True)
                        batches = division_object.batch_set.all()

                        timetable = sorted(
                            DateTimetable.objects.filter(Q(date=selected_date),
                                                         Q(original__division=division_object) | Q(
                                                             substitute__division=division_object),
                                                         is_active=True),
                            key=lambda x: (x.date, x.original.time.starting_time))

                        subjects = FacultySubject.objects.filter(faculty=user.faculty, subject__is_elective_group=False,
                                                                 elective_division=None,
                                                                 elective_subject=None, division=division_object,
                                                                 is_active=True)

                        subject_category = {'theory': [], 'practical': []}
                        for sub in subjects:
                            if sub.subject.is_practical is True:
                                subject_category['practical'] += [sub.subject.short_form]
                            else:
                                subject_category['theory'] += [sub.subject.short_form]

                        subjects = subjects.values_list('subject__short_form', flat=True).distinct()

                    else:
                        # elective division
                        splitted = division.split('--')
                        subject_selected = BranchSubject.objects.get(year_branch=year_branch_object,
                                                                     subject__is_elective_group=True,
                                                                     subject__short_form=splitted[
                                                                         0]).subject  # semester se bhi filter krna hai
                        elective_subject = ElectiveSubject.objects.get(short_form=splitted[1], subject=subject_selected)
                        elective_division = ElectiveDivision.objects.get(elective_subject=elective_subject,
                                                                         division=splitted[2])

                        timetable = sorted(
                            DateTimetable.objects.filter(Q(date=selected_date),
                                                         (Q(original__elective_division=elective_division),
                                                          Q(original__elective_subject=elective_subject)) | (Q(
                                                             substitute__elective_division=elective_division), Q(
                                                             substitute__elective_subject=elective_subject)),
                                                         is_active=True),
                            key=lambda x: (x.date, x.original.time.starting_time))

                    time_slots = Time.objects.all()

                    return render(request, 'extra_lecture.html', {
                        'data': data,
                        'timetable': timetable,
                        'time_slots': time_slots,
                        'subjects': subjects,
                        'batches': batches,
                        'rooms': room_dict,
                        'subject_category': json.dumps(subject_category),
                        'selected_date': selected_date,
                        'selected_branch': branch,
                        'selected_year': year,
                        'selected_division': division
                    })

                else:
                    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    room = request.POST.get('room')
                    type = request.POST.get('subject_type')
                    subject = request.POST.get('subject')
                    time = request.POST.get('time')
                    branch = request.POST.get('branch')
                    year = request.POST.get('year')
                    division = request.POST.get('division')
                    selected_date = parse_date(request.POST.get('selected_date'))
                    time_obj = Time.objects.get(pk=time)
                    year_branch_object = YearBranch.objects.get(year__year=year, branch__branch=branch)

                    if '--' not in division:
                        if type == "theory":
                            room = Room.objects.get(branch__branch=branch, room_number=room, lab=False)
                            branch_subject = BranchSubject.objects.get(year_branch=year_branch_object,
                                                                       subject__short_form=subject,
                                                                       subject__is_active=True,
                                                                       subject__is_elective_group=False,
                                                                       subject__is_practical=False)
                            division_object = Division.objects.get(year_branch=year_branch_object,
                                                                   division=division,
                                                                   is_active=True)

                            existing = DateTimetable.objects.filter(Q(date=selected_date), Q(is_active=True),
                                                                    (Q(original__time=time_obj) | Q(
                                                                        substitute__time=time_obj)),
                                                                    (Q(original__day=days[selected_date.weekday()]) | Q(
                                                                        substitute__time=days[
                                                                            selected_date.weekday()])),
                                                                    (Q(original__division=division_object) | Q(
                                                                        substitute__division=division_object)))

                            if existing.__len__() == 0:
                                new_tt = Timetable.objects.create(room=room, time=time_obj,
                                                                  day=days[selected_date.weekday()],
                                                                  branch_subject=branch_subject, faculty=faculty,
                                                                  division=division_object,
                                                                  is_practical=False)

                                DateTimetable.objects.create(date=selected_date, original=new_tt)

                                # notify students
                                return render(request, 'extra_lecture.html', {
                                    'data': data,
                                    'success': 'Lecture has been scheduled and students of that division have been notified.',
                                })

                            elif existing.__len__() > 1:
                                return HttpResponse('Something\' wrong! Should never go here!')

                            else:
                                # notify existing[0].faculty
                                return render(request, 'extra_lecture.html', {
                                    'data': data,
                                    'info': 'The faculty teaching from ' + time_obj + 'to ' + division + ' division have been notified about your request',
                                })

                        else:
                            room = Room.objects.get(branch__branch=branch, room_number=room, lab=True)
                            branch_subject = BranchSubject.objects.get(year_branch=year_branch_object,
                                                                       subject__short_form=subject,
                                                                       subject__is_active=True,
                                                                       subject__is_elective_group=False,
                                                                       subject__is_practical=False)
                            division_object = Division.objects.get(year_branch=year_branch_object,
                                                                   division=division,
                                                                   is_active=True)
                            batch = Batch.objects.get(division=division_object, batch_name=request.POST.get('batch'))

                            existing = DateTimetable.objects.filter(Q(date=selected_date), Q(is_active=True),
                                                                    (Q(original__time=time_obj) | Q(
                                                                        substitute__time=time_obj)),
                                                                    (Q(original__batch=batch) | Q(
                                                                        substitute__batch=batch)),
                                                                    (Q(original__day=days[selected_date.weekday()]) | Q(
                                                                        substitute__time=days[
                                                                            selected_date.weekday()])),
                                                                    (Q(original__division=division_object) | Q(
                                                                        substitute__division=division_object)))

                            if existing.__len__() == 0:
                                new_tt = Timetable.objects.create(room=room, time=time_obj,
                                                                  day=days[selected_date.weekday()],
                                                                  branch_subject=branch_subject, faculty=faculty,
                                                                  division=division_object,
                                                                  is_practical=True, batch=batch)

                                DateTimetable.objects.create(date=selected_date, original=new_tt)

                                # notify students
                                return render(request, 'extra_lecture.html', {
                                    'data': data,
                                    'success': 'Practical has been scheduled and students of that division have been notified.',
                                })

                            elif existing.__len__() > 1:
                                return HttpResponse('Something\' wrong! Should never go here!')

                            else:
                                # notify existing[0].faculty
                                return render(request, 'extra_lecture.html', {
                                    'data': data,
                                    'info': 'The faculty teaching from ' + time_obj + 'to ' + division + ' division have been notified about your request',
                                })

                    else:
                        pass

        else:
            return redirect('/login/')
    else:
        return redirect('/login/')


def test_url(request):
    # branch_obj = Branch.objects.get(branch='Mechanical')
    # year_obj = CollegeYear.objects.get(year='TE')
    # year_branch = YearBranch.objects.get(year=year_obj,branch=branch_obj,is_active=True)
    # division_obj = Division.objects.filter(year_branch=year_branch)
    # students = StudentDetail.objects.filter(batch__division__in=division_obj)
    # batch_obj = Batch.objects.filter(division=division_obj.get(division='B'))
    # for each_student in students:
    #     each_student.batch = batch_obj[0]
    #     each_student.save()
    return HttpResponse('Done')


def setup_branch(request):
    class_active = 'setup'
    user = request.user
    if not user.is_anonymous:
        if has_role(user, 'faculty'):
            if request.method == "GET":
                return render(request, 'setup_branch.html', {
                    'number_of_branch': Branch.objects.count(),
                    'all_branches': Branch.objects.all(),
                    'class_active': class_active,

                })

            elif request.method == "POST":
                branch = request.POST.get('branch')
                branch = branch.title()
                if len(Branch.objects.filter(branch=branch)) > 0:
                    return render(request, 'setup_branch.html', {
                        'error': branch + ' is already registered.',
                        'all_branches': Branch.objects.all(),
                        'number_of_branch': Branch.objects.count(),
                        'class_active': class_active,

                    })
                Branch.objects.create(branch=branch)
                return render(request, 'setup_branch.html', {
                    'success': 'Successfully registered ' + branch + ' branch',
                    'all_branches': Branch.objects.all(),
                    'number_of_branch': Branch.objects.count(),
                    'class_active': class_active,

                })

        return redirect('/login/')
    return redirect('/login/')


def setup_year(request):
    class_active = 'setup'
    user = request.user
    if not user.is_anonymous:
        branches = Branch.objects.all()
        if request.method == 'GET':
            return render(request, 'setup_year.html', {
                'class_active': class_active,
                'branches': branches,
                'number_of_year_branch': YearBranch.objects.count()
            })
        elif request.method == 'POST':
            year = request.POST.get('year')
            branch = request.POST.get('branch')

            no_of_sem = request.POST.get('no_of_sem')
            # for i in range(int(no_of_sem)):
            #     Semester.objects.create(semester=i+1)
            year_number = request.POST.get('year_number')

            year_obj = CollegeYear.objects.get_or_create(year=year, no_of_semester=no_of_sem, number=year_number)
            branch_obj = Branch.objects.get(branch=branch)
            for i in range(int(no_of_sem)):
                try:
                    sem_obj = Semester.objects.get(semester=i + 1, is_active=True)
                    # print(i+1, 'try')
                except:
                    sem_obj = Semester.objects.create(semester=i + 1)
                    # print(i+1, 'except')
                year_branch_obj = YearBranch.objects.get_or_create(year=year_obj[0], branch=branch_obj, is_active=True)
                YearSemester.objects.get_or_create(semester=sem_obj, year_branch=year_branch_obj[0])

                for i in range(int(request.POST.get('no_of_shift'))):
                    Shift.objects.get_or_create(year_branch=year_branch_obj[0], shift=(i + 1))

            return render(request, 'setup_year.html', {
                'class_active': class_active,
                'branches': branches,
                'success': 'Year ' + year + ' Saved!',
                'number_of_year_branch': YearBranch.objects.count()
            })
        return HttpResponse('Something is wrong!')
    return HttpResponseRedirect('/login/')


def setup_division(request):
    class_active = 'setup'
    user = request.user
    if not user.is_anonymous:
        if has_role(user, 'faculty'):
            data = {}
            year_branch = YearBranch.objects.filter(is_active=True)
            for each in year_branch:
                if each.branch.branch not in data:
                    data[each.branch.branch] = {}

                data[each.branch.branch][each.year.year] = each.shift_set.count()

            if request.method == "GET":
                return render(request, 'setup_division.html', {
                    'class_active': class_active,
                    'data': data,
                })
            else:
                print(request.POST)
                branch = Branch.objects.get(branch=request.POST.get('branch'))
                year = CollegeYear.objects.get(year=request.POST.get('year'))
                year_branch_obj = YearBranch.objects.get(branch=branch, year=year)
                divisions = request.POST.getlist('division')
                shifts = request.POST.getlist('shift')

                for index, value in enumerate(divisions):
                    Division.objects.get_or_create(year_branch=year_branch_obj, division=value,
                                                   shift=Shift.objects.get(year_branch=year_branch_obj,
                                                                           shift=shifts[index]))

            return render(request, 'setup_division.html', {
                'success': str(divisions) + 'registered',
                'class_active': class_active,
                'data': data,
            })

        return HttpResponse('Something is wrong!')
    return HttpResponseRedirect('/login/')


def setup_time(request):
    user = request.user
    if not user.is_anonymous:
        if has_role(user, 'faculty'):
            if request.method == "GET":
                return render(request, 'setup_time.html', {
                    'time_slots': Time.objects.all()
                })
            else:
                splitted_start_time = request.POST.get('start_time').split(':')
                splitted_end_time = request.POST.get('end_time').split(':')

                start_time = (int(splitted_start_time[0]) * 100) + int(splitted_start_time[1])
                end_time = (int(splitted_end_time[0]) * 100) + int(splitted_end_time[1])

                if len(Time.objects.filter(starting_time=start_time, ending_time=end_time)) > 0:
                    return render(request, 'setup_time.html', {
                        'error': 'Time slot already registered',
                        'time_slots': Time.objects.all()
                    })

                Time.objects.create(starting_time=start_time, ending_time=end_time)
                return render(request, 'setup_time.html', {
                    'success': 'Time slot registered',
                    'time_slots': Time.objects.all()
                })

        return redirect('/login/')
    return redirect('/login/')
