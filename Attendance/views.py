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
from .models import StudentAttendance, DailyAttendance


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
            faculty_subject_list = faculty.facultysubject_set.all()
            return render(request, "attendance.html", {
                'all_students': all_students,
                'selected_faculty_subject': selected_class_obj,
                'faculty_subject': faculty_subject_list
            })


        else:

            # should be faculty....alert on login page with proper message.

            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')


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
                faculty_subject = FacultySubject.objects.get(pk=int(request.POST.get('selected_faculty_subject')))
                division_obj = faculty_subject.division
                all_students = StudentDivision.objects.filter(division=division_obj).values_list('student__pk',
                                                                                                 flat=True)
                # all_students = StudentDetails.objects.all().values_list('pk', flat=True)
                print(all_students)
                print(request.POST)
                print("present")
                # present = [int(each) for each in present]
                print(present)
                absent = list(set(all_students) - set(present))
                print(absent)
                whole = []
                whole_daily = []
                for student in present:
                    print(faculty_subject, Student.objects.get(pk=student))
                    new = StudentAttendance(student=Student.objects.get(pk=student), faculty_subject=faculty_subject)
                    whole.append(new)
                    new.save()
                    new_daily = DailyAttendance(attendance=new, date=datetime.datetime.today(), attended=True)
                    whole_daily.append(new_daily)
                for student in absent:
                    new = StudentAttendance(student=Student.objects.get(pk=student), faculty_subject=faculty_subject)
                    whole.append(new)
                    new.save()
                    new_daily = DailyAttendance(attendance=new, date=datetime.datetime.today(), attended=False)
                    whole_daily.append(new_daily)
                print(whole_daily)
                print(whole)
                # StudentAttendance.objects.bulk_create(whole)
                DailyAttendance.objects.bulk_create(whole_daily)
                # print(request.POST.get)
                # all_students = StudentDetails.objects.all().values_list('id')
                # for i in request.POST:
                #     if i!='csrfmiddlewaretoken':
                #         print(i)

                # if i!=
            else:
                print("Not here because of post")
            return HttpResponse("Here")
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
            else:
                faculty = user.faculty
                faculty_subject_list = faculty.facultysubject_set.all()
                print(FacultySubject.objects.filter(faculty=user.faculty))
                return render(request, 'select_cat.html', {'faculty_subject': faculty_subject_list})

        else:
            # should be faculty....alert on login page with proper message.
            return HttpResponseRedirect('/login/')
    else:
        print('user no logged in')
        return HttpResponseRedirect('/login/')
