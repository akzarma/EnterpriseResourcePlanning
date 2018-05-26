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
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt

from Attendance.models import StudentAttendance
from Dashboard.models import SpecificNotification
from General.models import Batch, StudentDetail, Division, CollegeYear, FacultySubject, BranchSubject
from General.views import notify_users
from Registration.forms import StudentForm, FacultyForm
from Registration.models import Student, Branch, Faculty
import datetime

# Student dashboard
from Research.models import Paper
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
    user = request.user
    # If user exists in session (i.e. logged in)
    if not user.is_anonymous:
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        is_faculty = RoleManager.objects.filter(user=user, role__role='faculty')
        is_student = RoleManager.objects.filter(user=user, role__role='student')
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

            if request.method == "GET":
                date_range = [datetime.date.today() + datetime.timedelta(n) for n in [-1, 0, 1]]

                college_extra_detail = StudentDetail.objects.get(student=student, is_active=True).batch.division
                timetable = sorted(
                    DateTimetable.objects.filter(date__in=date_range, original__division=college_extra_detail),
                    key=lambda x: (x.date, x.original.time.starting_time))

                return render(request, 'dashboard_student.html', {
                    'timetable': timetable,
                    'date_range': date_range,
                    'days': days,
                    'total_attendance': total_percent,
                    'attendance': attendance,
                    'current_date': datetime.date.today().strftime('%Y-%m-%d'),
                })
            else:
                current_date = parse_date(request.POST.get('current_date'))
                # current_date = datetime.datetime.strptime(request.POST.get('current_date'), '%Y-%m-%d')
                if request.POST.get('previous'):
                    current_date = current_date + datetime.timedelta(-3)

                if request.POST.get('next'):
                    current_date = current_date + datetime.timedelta(3)

                date_range = [current_date + datetime.timedelta(n) for n in [-1, 0, 1]]

                college_extra_detail = StudentDetail.objects.get(student=student, is_active=True).batch.division
                timetable = sorted(
                    DateTimetable.objects.filter(date__in=date_range, original__division=college_extra_detail),
                    key=lambda x: (x.date, x.original.time.starting_time))

                return render(request, 'dashboard_student.html', {
                    'timetable': timetable,
                    'date_range': date_range,
                    'days': days,
                    'total_attendance': total_percent,
                    'attendance': attendance,
                    'current_date': current_date.strftime('%Y-%m-%d'),
                })

        elif is_faculty:
            faculty = user.faculty

            if request.method == "GET":
                timetable = sorted(
                    DateTimetable.objects.filter(date=datetime.date.today(), original__faculty=faculty),
                    key=lambda x: (x.date, x.original.time.starting_time))
                return render(request, 'dashboard_faculty.html', {
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
        if request.method == 'POST':
            is_faculty = RoleManager.objects.filter(user=user, role__role='faculty')
            is_student = RoleManager.objects.filter(user=user, role__role='student')
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


def get_excel(request):
    all_students = Student.objects.all()

    workbook = xlsxwriter.Workbook('Students.xlsx')
    worksheet = workbook.add_worksheet()

    all_fields = Student._meta._get_fields(reverse=False, include_parents=False)

    heading = [each.column for each in all_fields if
               each.related_model is None and each.get_internal_type() != 'FileField']

    start_index = 1

    row = 0
    worksheet.write(row, 0, 'Sr No.')

    for index in range(len(heading)):
        worksheet.write(row, index + start_index, heading[index])

    row = 1

    for row_index in range(len(all_students)):

        worksheet.write(row + row_index, 0, row_index + 1)

        for col_index in range(len(heading)):
            worksheet.write(row + row_index, start_index + col_index,
                            getattr(all_students[row_index], heading[col_index]))

    return HttpResponse('Done')


def excel_timetable(request):
    timetable_json = {}

    college_extra_detail = Division.objects.all()

    for each in college_extra_detail:
        branch = each.year_branch.branch.branch
        year = each.year_branch.year.year
        division = each.division

        if branch in timetable_json:
            if year in timetable_json[branch]:
                {}
            else:
                timetable_json[branch][year] = []
        else:
            timetable_json[branch] = {}
            timetable_json[branch][year] = []

        timetable_json[branch][year].append(division)

    return render(request, 'excel_timetable.html', {
        'timetable': timetable_json
    })


# @login_required
def download_excel_timetable(request):
    if request.method == 'GET':
        branch = request.GET.get('branch')
        year = request.GET.get('year')
        division = request.GET.get('division')

        full_timetable = Timetable.objects.all()

        college_extra_detail = Division.objects.all()

        if branch != 'all':
            branch_obj = Branch.objects.get(branch=branch)
            college_extra_detail = college_extra_detail.filter(year_branch__branch=branch_obj)

        if year != 'all':
            year_obj = CollegeYear.objects.get(year=year)
            college_extra_detail = college_extra_detail.filter(year_branch__year=year_obj)

        if division != 'all':
            college_extra_detail = college_extra_detail.filter(division=division)

        full_timetable = full_timetable.filter(division__in=college_extra_detail)

        generate_excel_from_query_set(full_timetable, 'timetable' + branch + '_' + year + '_' + division)

    return HttpResponse('Done')


def generate_excel_from_query_set(full_timetable, file_name, is_room=False, room_number='', param1='room',
                                  param2='faculty',
                                  param3='subject'):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    # branch_obj = Branch.objects.get(branch='Computer')
    # full_timetable = Timetable.objects.filter(branch_subject__branch=branch_obj)

    answer = OrderedDict()

    for each in sorted(full_timetable,
                       key=lambda x: (days.index(x.day), x.division.year_branch.year.number, x.time.starting_time)):
        year = each.branch_subject.year_branch.year.year
        branch = each.branch_subject.year_branch.branch.branch

        division = each.division.division

        day = each.day

        time = each.time

        faculty = each.faculty.initials

        room = each.room.room_number
        subject = each.branch_subject.subject.short_form

        if day in answer:
            if year in answer[day]:
                if division in answer[day][year]:
                    if time in answer[day][year][division]:
                        OrderedDict()
                    else:
                        answer[day][year][division][time] = OrderedDict()
                else:
                    answer[day][year][division] = OrderedDict()
                    answer[day][year][division][time] = OrderedDict()
            else:
                answer[day][year] = OrderedDict()
                answer[day][year][division] = OrderedDict()
                answer[day][year][division][time] = OrderedDict()
        else:
            answer[day] = OrderedDict()
            answer[day][year] = OrderedDict()
            answer[day][year][division] = OrderedDict()
            answer[day][year][division][time] = OrderedDict()

        is_practical = each.is_practical

        if is_practical:
            batch = each.batch.batch_name
            if 'is_practical' in answer[day][year][division][time]:
                {}
            else:
                answer[day][year][division][time] = {
                    'is_practical': is_practical
                }

            answer[day][year][division][time][batch] = {
                'faculty': faculty,
                'room': room,
                'subject': subject,
                'year': year + division
            }


        else:
            answer[day][year][division][time] = {
                'faculty': faculty,
                'room': room,
                'subject': subject,
                'is_practical': is_practical,
                'year': year + division
            }

    answer = OrderedDict(sorted(answer.items(), key=lambda x: days.index(x[0])))

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(file_name + '.xlsx')
    worksheet = workbook.add_worksheet()

    col = 1

    year_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow'})

    subject_format = workbook.add_format({
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#f0bfff'})
    time_format = workbook.add_format({
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'color': 'red'})

    practical_format = workbook.add_format({
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#77abff'})

    full_time = [each.__str__() for each in sorted(Time.objects.all(), key=lambda x: x.starting_time)]

    multiplier = 8

    if is_room:
        multiplier = 4

    for each_day in answer.items():

        merge_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'red'})

        row = 1
        temp = col

        # each_year_sorted = [each[0] for each in each_day[1].items()]

        for each_year in each_day[1].items():
            for each_division in each_year[1].items():
                if is_room == False:
                    worksheet.merge_range(row, temp, row, temp + 1, each_year[0] + each_division[0], year_format)
                else:
                    worksheet.merge_range(row, temp, row, temp + 1, room_number, year_format)

                each_division_sorted = OrderedDict(
                    sorted(each_division[1].items(), key=lambda x: x[0].starting_time))
                row = 2
                temp_row = row
                for each_time in each_division_sorted.items():

                    temp_row = full_time.index(each_time[0].__str__()) * multiplier + row

                    if not each_time[1]['is_practical']:
                        worksheet.merge_range(temp_row, temp, temp_row + int(multiplier / 2) - 1, temp,
                                              each_time[1][param1],
                                              subject_format)
                        worksheet.merge_range(temp_row, temp + 1, temp_row + int(multiplier / 2) - 1, temp + 1,
                                              str(each_time[1][param2]),
                                              subject_format)

                        worksheet.merge_range(temp_row + int(multiplier / 2), temp, temp_row + multiplier - 1,
                                              temp + 1, each_time[1][param3],
                                              subject_format)
                        # temp_row += 8
                        # workbook.close()
                        # print('here')
                        # workbook.close()
                    else:
                        for each_key in sorted(each_time[1].keys()):
                            if not each_key == 'is_practical':
                                worksheet.write(temp_row, temp, each_key, practical_format)
                                worksheet.write(temp_row, temp + 1, each_time[1][each_key][param3],
                                                practical_format)
                                worksheet.write(temp_row + 1, temp, each_time[1][each_key][param1],
                                                practical_format)
                                worksheet.write(temp_row + 1, temp + 1, each_time[1][each_key][param2],
                                                practical_format)
                                temp_row += 2

                if is_room == False:
                    temp += 2
                row = 1
        if is_room:
            temp += 2
        row = 0
        worksheet.merge_range(0, col, 0, temp - 1, each_day[0], merge_format)
        col = temp

    row_offset = 2
    col_offset = 0

    row = 0
    col = 0

    worksheet.write(row, col, 'Time')

    # Set time
    for each_time in full_time:
        worksheet.merge_range(row + row_offset, col + col_offset, row + row_offset + multiplier - 1, col + col_offset,
                              each_time, time_format)
        worksheet.set_column(col + col_offset, col + col_offset, len(str(each_time)))
        row += multiplier

    workbook.close()
    # workbook.filename()


def excel_room_schedule(request):
    branch = Branch.objects.all()

    branch_room_json = {}

    for each_branch in branch:
        branch_room_json[each_branch.branch] = list(set(each_branch.room_set.values_list('room_number', flat=True)))

    return render(request, 'excel_room_schedule.html', {
        'branch_room_json': branch_room_json
    })


def download_excel_room_schedule(request):
    # Code for all is remaining
    if request.is_ajax():
        branch = request.POST.get('branch')

        room = request.POST.get('room')

        full_timetable = Timetable.objects.all()

        if branch != 'all':
            branch_obj = Branch.objects.get(branch=branch)

            college_extra_detail = Division.objects.filter(year_branch__branch=branch_obj)

            full_timetable = full_timetable.filter(division__in=college_extra_detail)
            if room != 'all':
                room_obj = Room.objects.filter(branch=branch_obj, room_number=room)
                full_timetable = full_timetable.filter(room__in=room_obj)
                filename = 'room_schedule' + '_' + branch + '_' + room
                generate_excel_from_query_set(full_timetable, filename, True, room, 'year')
                return HttpResponse(filename)
            else:
                all_rooms = set(branch_obj.room_set.all().values_list('room_number', flat=True))
                data = []
                for each_room in all_rooms:
                    room_obj = Room.objects.filter(branch=branch_obj, room_number=each_room)
                    temp_timetable = full_timetable.filter(room__in=room_obj)
                    filename = 'room_schedule' + '_' + branch + '_' + each_room
                    generate_excel_from_query_set(temp_timetable, filename, True, each_room, 'year')
                    data.append(filename)
                return HttpResponse(json.dumps(data))
    else:
        return HttpResponseBadRequest('Not get')


def get_timetable(request):
    faculty = request.user.faculty
    selected_date = datetime.datetime.strptime(request.POST.get('selected_date'), '%m-%d-%Y').date()
    timetable = sorted(
        DateTimetable.objects.filter(date=selected_date, original__faculty=faculty),
        key=lambda x: (x.date, x.original.time.starting_time))

    return HttpResponse(timetable)


def excel_attendance(request):
    timetable_json = {}

    college_extra_detail = Division.objects.all()

    for each in college_extra_detail:
        branch = each.year_branch.branch.branch
        year = each.year_branch.year.year
        division = each.division

        if branch in timetable_json:
            if year in timetable_json[branch]:
                {}
            else:
                timetable_json[branch][year] = []
        else:
            timetable_json[branch] = {}
            timetable_json[branch][year] = []

        timetable_json[branch][year].append(division)

    print(timetable_json)

    return render(request, 'excel_attendance.html', {
        'timetable': timetable_json
    })


def download_excel_attendance_subject(request):
    if request.is_ajax():
        return HttpResponse('Done')


def toggle_availability(request):
    selected_timetable = DateTimetable.objects.get(pk=request.POST.get('selected_timetable'))
    send_notification = False
    if selected_timetable.not_available is True:
        if selected_timetable.is_substituted is False:
            selected_timetable.not_available = False
        else:
            if request.user.faculty == selected_timetable.substitute.faculty:
                selected_timetable.is_substituted = False
                send_notification = True
            else:
                return HttpResponse(
                    'Sorry, ' + selected_timetable.substitute.faculty.initials + ' has already taken your lecture!')
    else:
        selected_timetable.not_available = True
        send_notification = True

    if send_notification:
        selected_timetable.save()
        timetable_obj = selected_timetable.original
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
        notify_users(notification_type, message, heading, users_obj, type, action)

    return HttpResponse('success')


def get_notifications(request):
    user = request.user
    if not user.is_anonymous:
        if request.is_ajax():
            date = datetime.date.today().strftime('%Y-%m-%d')
            notification_objs = SpecificNotification.objects.filter(user=user, is_active=True, has_read=False)

            data = {'today': date}
            for each in range(len(notification_objs)):
                if not each in data:
                    data[each] = serializers.serialize('json', [notification_objs[each], ], fields=(
                        'heading', 'datetime', 'type', 'notification', 'has_read', 'action', 'priority'))
                    struct = json.loads(data[each])
                    data[each] = json.dumps(struct[0])

            return HttpResponse(json.dumps(data))

        else:
            return HttpResponse("Not ajax.Should be ajax")
    else:
        return redirect('/login/')


@csrf_exempt
def android_toggle_availability(request):
    return HttpResponse("Yeah!")


def show_all_notifications(request, page=1):
    user = request.user
    if not user.is_anonymous:
        is_faculty = RoleManager.objects.filter(user=user, role__role='faculty')
        if is_faculty:
            notification_objs = sorted(SpecificNotification.objects.filter(user=user), key=lambda x: x.datetime,
                                       reverse=True)[
                                (int(page) - 1) * 50:50]
            pages = SpecificNotification.objects.count()
            pages = pages // 50
            pages += 1 if pages % 50 is not 0 else 0
            if pages == 0:
                pages = 1

            # return render(request, 'all_notifications.html', {
            #     'notifications': notification_objs,
            #     'pages': range(1, pages + 1),
            #     'current_page': int(page),
            # })
            return render(request, 'all_categories_notification.html', {
                'notifications': notification_objs,
                'pages': range(1, pages + 1),
                'current_page': int(page),
            })
        return HttpResponseRedirect('/login/')
    return HttpResponseRedirect("/login/")


def view_notification(request):
    notification = SpecificNotification.objects.get(pk=int(request.POST.get('pk')))
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
    date = datetime.datetime.now().__str__()
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


def read_all_notification(request):
    pk = json.loads(request.POST.get('pk'))
    for each in pk:
        notification = SpecificNotification.objects.get(pk=int(each))
        notification.has_read = True
        notification.save()
    return HttpResponse("Done")
