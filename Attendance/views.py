# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from General.models import CollegeYear, CollegeExtraDetail, StudentDivision
from Registration.models import Student, Subject, Branch
from General.models import FacultySubject, StudentDivision
from Registration.models import Student, Subject, Faculty
from General.models import FacultySubject
from Registration.models import Student, Subject
from Timetable.models import Timetable
from .models import StudentAttendance


# Create your views here.
def index(request):
    # user = request.user
    # selected_faculty_subject = request.POST.get('selected_faculty_subject')
    # faculty = user.faculty
    # faculty_subject_list = faculty.facultysubject_set.all()
    # print(FacultySubject.objects.filter(faculty=user.faculty))
    # selected_faculty_subject_obj = FacultySubject.objects.get(pk=selected_faculty_subject)
    # faculty = user.faculty
    # all_students = StudentDivision.objects.filter(division=selected_faculty_subject_obj.division).all()
    user = request.user
    if not user.is_anonymous:
        if user.role == 'Faculty':
            faculty = user.faculty
            selected_class = request.POST.get('selected_class')
            selected_class_obj = Timetable.objects.get(pk=selected_class)
            all_students = StudentDivision.objects.filter(division=selected_class_obj.division).values_list(
                'student', flat=True)
            print(FacultySubject.objects.filter(faculty=user.faculty))
            timetables = faculty.timetable_set.all()
            return render(request, "attendance.html", {
                'all_students': all_students,
                'selected_class': selected_class_obj,
                'faculty_subject': timetables
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
                print("Saving Student")
                present = request.POST.getlist('present')
                print("present student list")
                print(present)
                print(request.POST)
                timetable = Timetable.objects.get(pk=int(request.POST.get('selected_class')))
                division_obj = timetable.division
                all_students = StudentDivision.objects.filter(division=division_obj).values_list('student__pk', flat=True)
                # all_students = StudentDetails.objects.all().values_list('pk', flat=True)
                print(all_students)
                print(request.POST)
                print("present")
                # present = [int(each) for each in present]
                print(present)
                absent = list(set(all_students) - set(present))
                print(absent)
                whole = []
                for student in present:
                    print(timetable, Student.objects.get(pk=student))
                    new = StudentAttendance(student=Student.objects.get(pk=student), timetable=timetable,
                                            attended=True, date=datetime.datetime.today())
                    whole.append(new)
                for student in absent:
                    new = StudentAttendance(student=Student.objects.get(pk=student), timetable=timetable,
                                            attended=False, date=datetime.datetime.today())
                    whole.append(new)
                print(whole)
                # StudentAttendance.objects.bulk_create(whole)
                StudentAttendance.objects.bulk_create(whole)

                faculty = user.faculty
                timetables = faculty.timetable_set.all()
                return render(request, 'select_cat.html', {'success': 'Attendance saved successfully',
                                                           'faculty_subject': timetables})

            else:
                return HttpResponseRedirect('/attendance/select')

        else:
            print('User not faculty')
            print(user.role)
            return HttpResponse('User not faculty')

    else:
        print('user not logged in')
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
                print(timetables)
                return render(request, 'select_cat.html', {'faculty_subject': timetables})

        else:
            # should be faculty....alert on login page with proper message.
            return HttpResponseRedirect('/login/')
    else:
        print('user no logged in')
        return HttpResponseRedirect('/login/')


def check_attendance(request):
    user = request.user
    if not user.is_anonymous:
        if user.role == 'Faculty':
            if request.method == 'POST':
                faculty = user.faculty
                current_tt = request.POST.get('selected_class')
                current_tt_obj = Timetable.objects.get(pk=current_tt)
                all_students = StudentAttendance.objects.filter(timetable=current_tt_obj,date=datetime.datetime.today())
                return render(request, "check_attendance.html", {
                    'all_students': all_students,
                })
            elif request.method == "GET":
                faculty = user.faculty
                timetables = faculty.timetable_set.all()
                print(timetables)
                return render(request, 'select_cat.html', {'faculty_subject': timetables, 'check': 1})
