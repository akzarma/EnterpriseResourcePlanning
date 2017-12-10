# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.http import HttpResponse
from django.shortcuts import render

from General.models import CollegeYear, CollegeExtraDetail, StudentDivision
from Registration.models import Student, Subject, Branch
from General.models import FacultySubject, StudentDivision
from Registration.models import Student, Subject, Faculty
from General.models import FacultySubject
from Registration.models import Student, Subject
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
            selected_faculty_subject = request.POST.get('selected_faculty_subject')
            selected_faculty_subject_obj = FacultySubject.objects.get(pk=selected_faculty_subject)
            all_students = StudentDivision.objects.filter(division=selected_faculty_subject_obj.division).all()
            print(FacultySubject.objects.filter(faculty=user.faculty))
            faculty_subject_list = faculty.facultysubject_set.all()
            return render(request, "attendance.html", {
                'all_students': all_students,
                'selected_faculty_subject': selected_faculty_subject_obj,
                'faculty_subject': faculty_subject_list
            })

        else:
            return HttpResponse("Not Faculty")
    else:
        return HttpResponse("Not Logged in.")


def save(request):
    user = request.user

    if user is not user.is_anonymous:
        if user.role == 'Faculty':
            if request.method == 'POST':
                faculty = user.faculty
                print("Saving Student")
                present = request.POST.getlist('present')
                print("present student list")
                print(present)
                subject = Subject.objects.get(code=int(request.POST.get('subject')))  # Get subject by pk(code)
                division = request.POST.get('division')
                year = request.POST.get('year')
                branch = request.POST.get('branch')
                branch_obj = Branch.objects.get(branch=branch)
                year_obj = CollegeYear.objects.get(year=year)
                division_obj = CollegeExtraDetail(year=year_obj,branch=branch_obj,division = division)
                all_students = StudentDivision.objects.filter(division=division_obj).values_list('pk',flat=True)
                # all_students = StudentDetails.objects.all().values_list('pk', flat=True)
                print(all_students)
                print(request.POST)
                print("present")
                present = [int(each) for each in present]
                print(present)
                absent = list(set(all_students) - set(present))
                print(absent)
                whole = []
                whole_daily = []
                for student in present:
                    new = StudentAttendance(student=Student.objects.get(pk=student), subject=subject,
                                            division=division)
                    whole.append(new)
                    new.save()
                    new_daily = DailyAttendance(attendance=new, date=datetime.datetime.today(), attended=True)
                    whole_daily.append(new_daily)
                for student in absent:
                    new = StudentAttendance(student=Student.objects.get(pk=student), subject=subject,
                                            division=division)
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
        print('user no logged in')
        return HttpResponse("User is not logged in")


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
            return HttpResponse("Not Faculty")
    else:
        return HttpResponse("Not Logged in.")
