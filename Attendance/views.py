# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db.models import Avg, Sum, Count
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils.dateparse import parse_date

from General.models import CollegeYear, CollegeExtraDetail, StudentDivision, BranchSubject
from Registration.models import Student, Subject, Branch, StudentRollNumber
from General.models import FacultySubject, StudentDivision
from Registration.models import Student, Subject, Faculty
from General.models import FacultySubject
from Registration.models import Student, Subject
from Timetable.models import Timetable
from .models import StudentAttendance, TotalAttendance


# Create your views here.
def index(request):
    user = request.user
    if not user.is_anonymous:
        if user.role == 'Faculty':
            faculty = user.faculty
            selected_class = request.POST.get('selected_class')
            selected_class_obj = Timetable.objects.get(pk=selected_class)
            selected_date = request.POST.get('selected_date')
            attendance = StudentAttendance.objects.filter(timetable=selected_class_obj,
                                                          date=parse_date(selected_date)).order_by('student__gr_number')
            if attendance:
                all_students = attendance
                att = 1
            else:
                all_students = StudentDivision.objects.filter(division=selected_class_obj.division) \
                    .values_list('student', flat=True).order_by('student__gr_number')
                att = 0
            timetables = faculty.timetable_set.all()
            return render(request, "attendance.html", {
                'all_students': all_students,
                'selected_class': selected_class_obj,
                'faculty_subject': timetables,
                'att': att,
                'selected_date': selected_date
            })


        else:

            # should be faculty....alert on login page with proper message.

            return render(request, 'login.html', {'info': 'That page is only for Faculty'})
    else:
        return render(request, 'login.html', {'error': 'Login first'})


def save(request):
    user = request.user

    if not user.is_anonymous:
        if user.role == 'Faculty':
            if request.method == 'POST':
                faculty = user.faculty
                present = request.POST.getlist('present')
                selected_date = request.POST.get('selected_date')

                timetable = Timetable.objects.get(pk=int(request.POST.get('selected_class')))
                division_obj = timetable.division
                all_students = StudentDivision.objects.filter(division=division_obj).values_list('student__pk',
                                                                                                 flat=True)
                # all_students = StudentDetails.objects.all().values_list('pk', flat=True)
                absent = list(set(all_students) - set(present))

                whole = []
                for student in present:
                    new = StudentAttendance.objects.filter(student=Student.objects.get(pk=student), timetable=timetable,
                                                           date=parse_date(selected_date)).first()
                    if new:
                        new.attended = True
                        new.save()
                    else:
                        new = StudentAttendance(student=Student.objects.get(pk=student), timetable=timetable,
                                                attended=True, date=parse_date(selected_date))
                        whole.append(new)
                for student in absent:
                    new = StudentAttendance.objects.filter(student=Student.objects.get(pk=student), timetable=timetable,
                                                           date=parse_date(selected_date)).first()
                    if new:
                        new.attended = False
                        new.save()
                    else:
                        new = StudentAttendance(student=Student.objects.get(pk=student), timetable=timetable,
                                                attended=False, date=parse_date(selected_date))
                        whole.append(new)
                # StudentAttendance.objects.bulk_create(whole)
                StudentAttendance.objects.bulk_create(whole)

                faculty = user.faculty
                timetables = faculty.timetable_set.all()
                return render(request, 'select_cat.html', {'success': 'Attendance saved successfully',
                                                           'faculty_subject': timetables})

            else:
                return HttpResponseRedirect('/attendance/select')

        else:
            return HttpResponse('User not faculty')

    else:
        return HttpResponseRedirect('/login/')


def select_cat(request):
    user = request.user
    if not user.is_anonymous:
        if user.role == 'Faculty':
            if request.method == 'POST':
                form = FacultySubject(request.POST, request.FILES, instance=user.faculty)
                return HttpResponse('Where are you going?')
            else:
                faculty = user.faculty
                timetables = faculty.timetable_set.all()
                return render(request, 'select_cat.html', {'faculty_subject': timetables})

        else:
            # should be faculty....alert on login page with proper message.
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')


def check_attendance(request):
    user = request.user
    if not user.is_anonymous:
        if user.role == 'Faculty':
            if request.method == 'POST':
                if request.POST.get('go'):
                    selected_date = request.POST.get('selected_date')
                    current_tt = request.POST.get('selected_class')
                    current_tt_obj = Timetable.objects.get(pk=current_tt)
                    count = 0
                    present_percent = 0
                    all_students = StudentAttendance.objects.filter(timetable=current_tt_obj,
                                                                    date=parse_date(selected_date)).order_by(
                        'student__gr_number')
                    count = all_students.filter(attended=True).count()

                    if all_students.count():
                        present_percent = count / all_students.count()
                    return render(request, "check_attendance.html", {
                        'all_students': all_students,
                        'present': present_percent * 100
                    })

                elif request.POST.get('check_attendance_button'):
                    selected_from_date = request.POST.get('selected_from_date')
                    selected_to_date = request.POST.get('selected_to_date')
                    selected_faculty_subject = request.POST.get('selected_subject')
                    selected_faculty_subject_obj = FacultySubject.objects.get(pk=selected_faculty_subject)
                    branch_subject_obj = BranchSubject.objects.get(subject=selected_faculty_subject_obj.subject,
                                                                   branch=selected_faculty_subject_obj.division.branch,
                                                                   year=selected_faculty_subject_obj.division.year,
                                                                   semester=1)
                    #
                    # Semester ko subject se lena hai
                    #
                    current_tt_obj = Timetable.objects.filter(faculty=selected_faculty_subject_obj.faculty,
                                                              division=selected_faculty_subject_obj.division,
                                                              branch_subject=branch_subject_obj)

                    lecture_percentage = 0
                    all_students_count = 0
                    all_students_present = 0
                    individual_attendance = {}

                    for i in StudentDivision.objects.filter(
                            division__branch=selected_faculty_subject_obj.division.branch,
                            division__year=selected_faculty_subject_obj.division.year,
                            division__division=selected_faculty_subject_obj.division.division,
                            division__shift=selected_faculty_subject_obj.division.shift):
                        individual_attendance[i.student.pk] = 0

                    count_present = 0
                    for i in current_tt_obj:  # For days in week
                        all_students_obj = StudentAttendance.objects.filter(timetable=i, date__range=(
                            selected_from_date, selected_to_date))  # For the day in every week in given date range
                        all_students_count += all_students_obj.count()
                        all_students_present += all_students_obj.filter(attended=True).count()

                        for j in all_students_obj:
                            if j.attended:
                                individual_attendance[j.student.pk] += 1

                    if all_students_count:
                        lecture_percentage += all_students_present / all_students_count * 100

                    return render(request, 'lecture_attendance.html',
                                  {'lecture_percent': "{0:.2f}".format(lecture_percentage),
                                   'selected_from_date': selected_from_date,
                                   'selected_to_date': selected_to_date,
                                   'individual_attendance': individual_attendance})

            elif request.method == "GET":
                faculty = user.faculty
                timetables = faculty.timetable_set.all()
                faculty_subject = FacultySubject.objects.filter(faculty=faculty)
                return render(request, 'select_check_attendance.html',
                              {'faculty_subject': timetables, 'subjects': faculty_subject})
        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')


def android_display_attendance(request):
    if request.method == 'POST':
        gr_number = request.POST.get('gr_number')

        if not gr_number:
            error = {
                'error': 'No GR number.'
            }
            return HttpResponse(error)

        student = Student.objects.get(gr_number=gr_number)

        total_attendance = student.totalattendance_set

        response = {}

        attended = 0
        total = 0

        for each in total_attendance:
            total += each.total_lectures
            attended += each.attended_lectures
            response[each.subject.short_form] = {
                'total': each.total_lectures,
                'attended': each.attended_lectures
            }
        total_percent = 100 * attended / total

        response['total_percent'] = total_percent
        return JsonResponse(response)

    else:
        error = {
            'error': 'Not Post.'
        }
        return HttpResponse(error)


def mark_from_excel(request):
    file = open('Attendance/Documents/TE_B_attendance.csv', 'r')

    full_text = file.read()

    each_line = full_text.split('\n')

    subjects = each_line[0].split(',')

    each_line.remove(each_line[0])
    each_line.remove(each_line[0])

    for each_student in each_line:

        token = each_student.split(',')
        roll = int(token[0])

        student = StudentRollNumber.objects.filter(roll_number=roll)

        if student:
            student = student[0].student
            for (each_subject, i) in zip(subjects, range(5)):

                lect = token[i + 2]

                lect_split = lect.split('/')

                attended = 0
                total = 0

                if lect_split != ['']:
                    # print(lect_split)
                    attended = int(lect_split[0])
                    total = int(lect_split[1])

                subject_obj = Subject.objects.get(code=each_subject)

                TotalAttendance.objects.create(student=student, subject=subject_obj, total_lectures=total,
                                               attended_leactures=attended)

        else:
            print(token[1])

    return HttpResponse("here")
