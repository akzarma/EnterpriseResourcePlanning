# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime

from django.http import HttpResponse
from django.shortcuts import render

from General.models import FacultySubject, StudentDivision
from Registration.models import Student, Subject, Faculty
from .models import StudentAttendance, DailyAttendance


# Create your views here.
def index(request):
    user = request.user
    selected_faculty_subject = request.POST.get('selected_faculty_subject')
    selected_faculty_subject_obj = FacultySubject.objects.get(pk=selected_faculty_subject)
    faculty_obj = Faculty.objects.get(user=user)
    all_students = StudentDivision.objects.filter(division=selected_faculty_subject_obj.division)
    all_subjects = [i.subject for i in FacultySubject.objects.filter(faculty=faculty_obj)]
    return render(request, "attendance.html", {
        'all_students': all_students,
        'all_subjects': all_subjects,
        'selected_subject' : selected_faculty_subject_obj.subject.short_form,
        'selected_division' : selected_faculty_subject_obj.division.division,
    })


def save(request):
    if request.method == 'POST':
        print("Saving Student")
        present = request.POST.getlist('present')
        subject = Subject.objects.get(pk=int(request.POST.get('subject')))
        division = request.POST.get('division')
        all_students = Student.objects.all().values_list('pk', flat=True)
        print(all_students)
        print(request.POST)
        print("present")
        for i in range(len(present)):
            present[i] = int(present[i])
        print(present)
        absent = list(set(all_students) - set(present))
        print(absent)
        whole = []
        whole_daily = []
        for student in present:
            new = StudentAttendance(student=Student.objects.get(pk=student), subject=subject, division=division)
            whole.append(new)
            new.save()
            new_daily = DailyAttendance(attendance=new, date=datetime.datetime.today(), attended=True)
            whole_daily.append(new_daily)
        for student in absent:
            new = StudentAttendance(student=Student.objects.get(pk=student), subject=subject, division=division)
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
