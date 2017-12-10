# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.http import HttpResponse
from django.shortcuts import render

from Registration.models import Student, Subject
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
    if request.method == 'POST':
        print("Saving Student")
        present = request.POST.getlist('present')
        subject = Subject.objects.get(pk=int(request.POST.get('subject')))
        division = request.POST.get('division')
        all_students = StudentDetails.objects.all().values_list('pk', flat=True)
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
            new = StudentAttendance(student=StudentDetails.objects.get(pk=student), subject=subject, division=division)
            whole.append(new)
            new.save()
            new_daily = DailyAttendance(attendance=new, date=datetime.datetime.today(), attended=True)
            whole_daily.append(new_daily)
        for student in absent:
            new = StudentAttendance(student=StudentDetails.objects.get(pk=student), subject=subject, division=division)
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
