# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.http import HttpResponse
from django.shortcuts import render

from General.models import CollegeYear, CollegeExtraDetail, StudentDivision
from Registration.models import Student, Subject, Branch
from .models import StudentAttendance, DailyAttendance


# Create your views here.
def index(request):
    all_students = Student.objects.all()
    all_subjects = Subject.objects.all()
    return render(request, "attendance.html", {
        'all_students': all_students,
        'all_subjects': all_subjects
    })


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
