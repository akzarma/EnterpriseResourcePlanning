import json, copy
from collections import OrderedDict
from itertools import chain

import xlsxwriter
from django import urls
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
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
from General.models import Batch, StudentDetail, Division, CollegeYear, FacultySubject, BranchSubject
from General.views import notify_users
from Registration.forms import StudentForm, FacultyForm
from Registration.models import Student, Branch, Faculty
import datetime

# Student dashboard
from Registration.views import has_role
from Research.models import Paper
from SelfConcept.models import Question
from Timetable.models import Timetable, DateTimetable, Time, Room
from Update.forms import StudentUpdateForm, FacultyUpdateForm
from UserModel.models import User, RoleMaster, RoleManager


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
            attended = 0
            total = 0
            total_attendance = student.totalattendance_set.all()

            for each in total_attendance:
                total += each.total_lectures
                attended += each.attended_lectures
                if each.total_lectures is not 0:
                    subject_attendance = round(100 * each.attended_lectures / each.total_lectures, 2)
                else:
                    subject_attendance = 0
                attendance[each.subject.short_form] = {
                    'total': each.total_lectures,
                    'attended': each.attended_lectures,
                    'attendance': subject_attendance,
                }
            total_percent = round(100 * attended / total, 2) if total is not 0 else 0

            college_extra_detail = StudentDetail.objects.get(student=student, is_active=True).batch.division
            if request.method == "GET":
                timetable = sorted(
                    DateTimetable.objects.filter(date=datetime.date.today(), original__division=college_extra_detail),
                    key=lambda x: (x.date, x.original.time.starting_time))

                return render(request, 'dashboard_student.html', {
                    'timetable': timetable,
                    'total_attendance': total_percent,
                    'attendance': attendance,
                    'selected_date': datetime.date.today().strftime('%d-%m-%Y'),
                })
            else:
                if 'GO' in request.POST:
                    selected_date = datetime.datetime.strptime(request.POST.get('selected_date'), '%d-%m-%Y').date()
                    timetable = sorted(
                        DateTimetable.objects.filter(date=selected_date,
                                                     original__division=college_extra_detail),
                        key=lambda x: (x.date, x.original.time.starting_time))

                    return render(request, 'dashboard_student.html', {
                        'timetable': timetable,
                        'total_attendance': total_percent,
                        'attendance': attendance,
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
                                                     original__division=college_extra_detail),
                        key=lambda x: (x.date, x.original.time.starting_time))

                    return render(request, 'dashboard_student.html', {
                        'timetable': timetable,
                        'total_attendance': total_percent,
                        'attendance': attendance,
                        'selected_date': selected_date.strftime('%d-%m-%Y'),
                    })

        elif is_faculty:
            faculty = user.faculty

            if request.method == "GET":
                timetable = sorted(
                    DateTimetable.objects.filter(date=datetime.date.today(), original__faculty=faculty),
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
                        DateTimetable.objects.filter(Q(date=selected_date),
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
                        DateTimetable.objects.filter(Q(date=selected_date),
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
                        DateTimetable.objects.filter(Q(date=selected_date),
                                                     Q(original__faculty=faculty) | Q(substitute__faculty=faculty)),
                        key=lambda x: (x.date, x.original.time.starting_time))

                    selected_class_obj = DateTimetable.objects.get(pk=request.POST.get('date_timetable'))

                    if selected_class_obj.original.is_practical:
                        attendance = StudentAttendance.objects.filter(
                            student__studentdetail__batch=selected_class_obj.original.batch,
                            timetable=selected_class_obj)

                        present_roll = sorted(
                            [StudentDetail.objects.get(student=each.student).roll_number for each in attendance if
                             each.attended is True])

                        all_students = StudentDetail.objects.filter(
                            batch=selected_class_obj.original.batch).values_list('student', flat=True)
                        all_students_roll = sorted(
                            [StudentDetail.objects.get(student=each, is_active=True).roll_number for
                             each in all_students])

                    else:
                        attendance = StudentAttendance.objects.filter(timetable=selected_class_obj)
                        present_roll = sorted([StudentDetail.objects.get(student=each.student).roll_number
                                               for each in attendance if each.attended is True])

                        all_students = StudentDetail.objects.filter(
                            batch__division=selected_class_obj.original.division) \
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
                    all_faculty_at_that_time.append((each_tt.original.faculty.user.username))

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
        notification_objs = sorted(SpecificNotification.objects.filter(user=user))[
                            (int(page) - 1) * NOTIFICATION_LONG_LIMIT:(int(
                                page) - 1) * NOTIFICATION_LONG_LIMIT + NOTIFICATION_LONG_LIMIT]
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

        final_notifications = sorted(all_notifications, key=lambda x: x.datetime)[:NOTIFICATION_LONG_LIMIT]

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
    return


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
    user = User.objects.get(username=request.POST.get('username'))
    notification_objs = SpecificNotification.objects.filter(user=user, is_active=True)

    data = {}
    for each in range(len(notification_objs)):
        if not each in data:
            data[each] = serializers.serialize('json', [notification_objs[each], ], fields=(
                'heading', 'datetime', 'type', 'notification', 'has_read', 'action', 'priority'))
            data[each] = json.loads(data[each])[0]
            # data[each] = json.dumps(struct[0])
    answer = {}
    answer['timeline'] = data
    return JsonResponse(data)


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
            return HttpResponse("Sorry, this lecture has already been taken by someone else.")

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

