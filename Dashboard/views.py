import json
from collections import OrderedDict
from itertools import chain

import xlsxwriter
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date

from General.models import Batch, StudentDetail, CollegeExtraDetail, CollegeYear
from Registration.forms import StudentForm, FacultyForm
from Registration.models import Student, Branch
import datetime

# Student dashboard
from Research.models import Paper
from Timetable.models import Timetable, DateTimetable, Time
from Update.forms import StudentUpdateForm, FacultyUpdateForm
from UserModel.models import User


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

        if user.role == 'Student':
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

        elif user.role == 'Faculty':
            faculty = user.faculty

            if request.method == "GET":
                date_range = [datetime.date.today() + datetime.timedelta(n) for n in [-1, 0, 1]]

                timetable = sorted(
                    DateTimetable.objects.filter(date__in=date_range, original__faculty=faculty),
                    key=lambda x: (x.date, x.original.time.starting_time))
                return render(request, 'dashboard_faculty.html', {
                    'timetable': timetable,
                    'date_range': date_range,
                    'days': days,
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

                timetable = sorted(
                    DateTimetable.objects.filter(date__in=date_range, original__faculty=faculty),
                    key=lambda x: (x.date, x.original.time.starting_time))
                return render(request, 'dashboard_faculty.html', {
                    'timetable': timetable,
                    'date_range': date_range,
                    'days': days,
                    'current_date': current_date.strftime('%Y-%m-%d')
                })
        else:
            logout_user(request)
            return redirect('/login/')
    else:
        return redirect('/login/')


def view_profile(request):
    user = request.user
    if not user.is_anonymous:
        if request.method == 'POST':
            if user.role == 'Student':
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

            elif user.role == 'Faculty':
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
            if user.role == 'Faculty':
                obj = user.faculty
                form = FacultyUpdateForm(instance=obj)
                return render(request, 'profile_faculty.html', {
                    'form': form,
                })

            elif user.role == 'Student':
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

    college_extra_detail = CollegeExtraDetail.objects.all()

    for each in college_extra_detail:
        branch = each.branch.branch
        year = each.year.year
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

        college_extra_detail = CollegeExtraDetail.objects.all()

        if branch != 'all':
            branch_obj = Branch.objects.get(branch=branch)
            college_extra_detail = college_extra_detail.filter(branch=branch_obj)

        if year != 'all':
            year_obj = CollegeYear.objects.get(year=year)
            college_extra_detail = college_extra_detail.filter(year=year_obj)

        if division != 'all':
            college_extra_detail = college_extra_detail.filter(division=division)

        full_timetable = full_timetable.filter(division__in=college_extra_detail)


        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

        # branch_obj = Branch.objects.get(branch='Computer')
        # full_timetable = Timetable.objects.filter(branch_subject__branch=branch_obj)

        answer = OrderedDict()

        for each in sorted(full_timetable,
                           key=lambda x: (days.index(x.day), x.division.year.number, x.time.starting_time)):
            year = each.branch_subject.year.year
            branch = each.branch_subject.branch.branch

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
                }


            else:
                answer[day][year][division][time] = {
                    'faculty': faculty,
                    'room': room,
                    'subject': subject,
                    'is_practical': is_practical
                }

        answer = OrderedDict(sorted(answer.items(), key=lambda x: days.index(x[0])))

        # Create a workbook and add a worksheet.
        workbook = xlsxwriter.Workbook('timetable_' + branch + '_' + year + '_' + division + '.xlsx')
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
                    worksheet.merge_range(row, temp, row, temp + 1, each_year[0] + each_division[0], year_format)

                    each_division_sorted = OrderedDict(
                        sorted(each_division[1].items(), key=lambda x: x[0].starting_time))
                    row = 2
                    temp_row = row
                    for each_time in each_division_sorted.items():

                        temp_row = full_time.index(each_time[0].__str__()) * 8 + row

                        if not each_time[1]['is_practical']:
                            worksheet.merge_range(temp_row, temp, temp_row + 3, temp, str(each_time[1]['room']),
                                                  subject_format)
                            worksheet.merge_range(temp_row, temp + 1, temp_row + 3, temp + 1,
                                                  str(each_time[1]['faculty']),
                                                  subject_format)

                            worksheet.merge_range(temp_row + 4, temp, temp_row + 7, temp + 1, each_time[1]['subject'],
                                                  subject_format)
                            # temp_row += 8

                        else:
                            for each_key in sorted(each_time[1].keys()):
                                if not each_key == 'is_practical':
                                    worksheet.write(temp_row, temp, each_key, practical_format)
                                    worksheet.write(temp_row, temp + 1, each_time[1][each_key]['subject'],
                                                    practical_format)
                                    worksheet.write(temp_row + 1, temp, each_time[1][each_key]['room'],
                                                    practical_format)
                                    worksheet.write(temp_row + 1, temp + 1, each_time[1][each_key]['faculty'],
                                                    practical_format)
                                    temp_row += 2

                    temp += 2
                    row = 1

            row = 0
            worksheet.merge_range(0, col, 0, temp - 1, each_day[0], merge_format)
            col = temp

        row_offset = 2
        col_offset = 0

        row = 0
        col = 0

        worksheet.write(row, col, 'Time')

        for each_time in full_time:
            worksheet.merge_range(row + row_offset, col + col_offset, row + row_offset + 7, col + col_offset,
                                  each_time, time_format)
            worksheet.set_column(col + col_offset, col + col_offset, len(str(each_time)))
            row += 8

        workbook.close()

    return HttpResponse('Done')
