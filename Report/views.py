import json, copy
import os
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
from Dashboard.models import SpecificNotification, GeneralStudentNotification, GeneralFacultyNotification
from EnterpriseResourcePlanning.settings import NOTIFICATION_LONG_LIMIT, NOTIFICATION_SMALL_LIMIT
from General.models import Batch, StudentDetail, Division, CollegeYear, FacultySubject, BranchSubject
from General.views import notify_users
from Registration.forms import StudentForm, FacultyForm
from Registration.models import Student, Branch, Faculty
import datetime

# Student dashboard
from Research.models import Paper
from Timetable.models import Timetable, DateTimetable, Time, Room
from Update.forms import StudentUpdateForm, FacultyUpdateForm
from UserModel.models import  RoleMaster, RoleManager


def student_details(request):
    class_active = "excel"
    if request.method == 'POST':
        all_students = Student.objects.all()
        directory = './Media/documents/StudentDetails/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        workbook = xlsxwriter.Workbook(directory + 'Students_' + datetime.date.today().__str__()
                                       + '_' + datetime.datetime.today().time().__str__() + '.xlsx')
        worksheet = workbook.add_worksheet()

        dark_gray = workbook.add_format()
        dark_gray.set_bg_color('#b2aeae')
        dark_gray.set_border(1)

        light_gray = workbook.add_format()
        light_gray.set_border(1)
        light_gray.set_bg_color('#f1eacf')
        fields = request.POST.getlist('fields')
        col = 1
        row = 1
        i = 0

        for each_field in fields:
            worksheet.write(row, col + i, each_field)
            i += 1

        col = 1
        row = 3
        i_row = 0
        i_col = 0

        for each_student in all_students:
            i_col = 0
            for each_field in fields:
                try:
                    if each_field == 'email':
                        worksheet.write(row + i_row, col + i_col, each_student.user.email,
                                        light_gray if i_row % 2 == 0 else dark_gray)
                    elif each_field == 'division':
                        worksheet.write(row + i_row, col + i_col,
                                        each_student.studentdetail_set.first().batch.division.division,
                                        light_gray if i_row % 2 == 0 else dark_gray)
                    elif each_field == 'year':
                        worksheet.write(row + i_row, col + i_col,
                                        each_student.studentdetail_set.first().batch.division.year_branch.year.year,
                                        light_gray if i_row % 2 == 0 else dark_gray)
                    elif each_field == 'batch':
                        worksheet.write(row + i_row, col + i_col,
                                        each_student.studentdetail_set.first().batch.batch_name,
                                        light_gray if i_row % 2 == 0 else dark_gray)
                    elif each_field == 'branch':
                        worksheet.write(row + i_row, col + i_col,
                                        each_student.studentdetail_set.first().batch.division.year_branch.bramch.branch,
                                        light_gray if i_row % 2 == 0 else dark_gray)
                    elif each_field == 'roll_number':
                        worksheet.write(row + i_row, col + i_col, each_student.studentdetail_set.first().roll_number,
                                        light_gray if i_row % 2 == 0 else dark_gray)
                    else:
                        worksheet.write(row + i_row, col + i_col, getattr(each_student, each_field),
                                        light_gray if i_row % 2 == 0 else dark_gray)
                except:
                    pass
                i_col += 1

            i_row += 1
        workbook.close()

        return render(request, 'student_details.html', {
            'class_active': class_active,
            'fields': StudentForm,
            'success': 'Done'})

    elif request.method == 'GET':
        return render(request, 'student_details.html', {
            'class_active': class_active,
            'fields': StudentForm,
        })


def get_excel(request):
    all_students = Student.objects.all()

    directory = './Media/documents/Students/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    workbook = xlsxwriter.Workbook(directory + 'StudentsEveryField.xlsx')
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


def get_timetable(request):
    faculty = request.user.faculty
    selected_date = datetime.datetime.strptime(request.POST.get('selected_date'), '%m-%d-%Y').date()
    timetable = sorted(
        DateTimetable.objects.filter(date=selected_date, original__faculty=faculty),
        key=lambda x: (x.date, x.original.time.starting_time))

    return HttpResponse(timetable)


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
    directory = './Media/documents/TimeTable/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    workbook = xlsxwriter.Workbook(directory + file_name + '.xlsx')
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
    class_active = "excel"
    branch_room_json = {}

    for each_branch in branch:
        branch_room_json[each_branch.branch] = list(set(each_branch.room_set.values_list('room_number', flat=True)))

    return render(request, 'excel_room_schedule.html', {
        'class_active': class_active,
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
            prefix = 'Media/documents/TimeTable/'
            full_timetable = full_timetable.filter(division__in=college_extra_detail)
            if room != 'all':
                room_obj = Room.objects.filter(branch=branch_obj, room_number=room)
                full_timetable = full_timetable.filter(room__in=room_obj)
                filename = 'room_schedule' + '_' + branch + '_' + room
                generate_excel_from_query_set(full_timetable, filename, True, room, 'year')
                return HttpResponse(prefix + filename)
            else:
                all_rooms = set(branch_obj.room_set.all().values_list('room_number', flat=True))
                data = []
                for each_room in all_rooms:
                    room_obj = Room.objects.filter(branch=branch_obj, room_number=each_room)
                    temp_timetable = full_timetable.filter(room__in=room_obj)
                    filename = 'room_schedule' + '_' + branch + '_' + each_room
                    generate_excel_from_query_set(temp_timetable, filename, True, each_room, 'year')
                    data.append(prefix + filename)
                return HttpResponse(json.dumps(data))
    else:
        return HttpResponseBadRequest('Not ajax')


def excel_attendance(request):
    timetable_json = {}
    class_active = "excel"
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
        'class_active': class_active,
        'timetable': timetable_json
    })


def download_excel_attendance_subject(request):
    if request.is_ajax():
        return HttpResponse('Done')


def excel_timetable(request):
    class_active = "excel"
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
        'class_active': class_active,
        'timetable': timetable_json
    })


def faculty_details(request):
    class_active = 'excel'
    if request.method == 'POST':
        all_faculties = Faculty.objects.all()
        directory = './Media/documents/FacultyDetails/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        workbook = xlsxwriter.Workbook(directory + 'Faculty_' + datetime.date.today().__str__()
                                       + '_' + datetime.datetime.today().time().__str__() + '.xlsx')
        worksheet = workbook.add_worksheet()

        dark_gray = workbook.add_format()
        dark_gray.set_bg_color('#b2aeae')
        dark_gray.set_border(1)

        light_gray = workbook.add_format()
        light_gray.set_border(1)
        light_gray.set_bg_color('#f1eacf')
        fields = request.POST.getlist('fields')
        col = 1
        row = 1
        i = 0

        for each_field in fields:
            worksheet.write(row, col + i, each_field)
            i += 1

        col = 1
        row = 3
        i_row = 0
        i_col = 0

        for each_faculty in all_faculties:
            i_col = 0
            for each_field in fields:
                try:
                    if each_field == 'email':
                        worksheet.write(row + i_row, col + i_col, each_faculty.user.email,
                                        light_gray if i_row % 2 == 0 else dark_gray)
                    else:
                        worksheet.write(row + i_row, col + i_col, getattr(each_faculty, each_field),
                                        light_gray if i_row % 2 == 0 else dark_gray)
                except:
                    pass
                i_col += 1

            i_row += 1
        workbook.close()

        return render(request, 'faculty_details.html', {
            'class_active': class_active,
            'fields': FacultyForm,
            'success': 'Done'})

    elif request.method == 'GET':
        class_active = 'excel'
        return render(request, 'faculty_details.html', {
            'class_active': class_active,
            'fields': FacultyForm,
        })
