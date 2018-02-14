from __future__ import unicode_literals

import json

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from General.models import StudentDivision
from Registration.models import Faculty, Student, Branch, StudentRollNumber
from Timetable.models import Timetable
from UserModel.models import User
import json


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/dashboard/')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    elif request.method == "GET":
        user = request.user
        if user.is_anonymous:
            return render(request, 'login.html')
        else:
            return HttpResponseRedirect('/dashboard/')

    return render(request, 'login.html')


@csrf_exempt
def login_android(request):
    response = {
        'user_type': 'null'
    }
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)

            if user:

                user = User.objects.get(username=username)
                if user.role == 'Faculty':
                    faculty = user.faculty
                    faculty_response = {
                        'user_type': 'Faculty',
                        'initials': user.faculty.initials,
                        'name': user.faculty.first_name
                    }
                    return HttpResponse(str(faculty_response))

                    all_divisions = [each.division for each in Timetable.objects.filter(faculty=faculty)]

                    attendance_list = {}

                    for each_division in all_divisions:

                        all_student = [each.student for each in StudentDivision.objects.filter(division=each_division)]

                        year = each_division.year.year

                        division = each_division.division
                        branch = each_division.branch.branch

                        if year in attendance_list:

                            if branch in attendance_list[year][division]:
                                if division in attendance_list[year]:

                                    var = {}
                                else:
                                    attendance_list[year][branch][division] = {}
                            else:
                                attendance_list[year][branch] = {}
                                attendance_list[year][branch][division] = {}

                        else:
                            attendance_list[year] = {}
                            attendance_list[year][branch] = {}
                            attendance_list[year][branch][division] = []
                        # attendance_list[year][branch][division] = sorted([
                        #     StudentRollNumber.objects.get(student=each_student.student, is_active=True) for
                        #     each_student in all_student])

                        for each_student in all_student:

                            roll_number = StudentRollNumber.objects.get(student=each_student,
                                                                        is_active=True).roll_number

                            attendance_list[year][branch][division].append(roll_number)

                    faculty_response['attendance_list'] = attendance_list

                    return HttpResponse(str(faculty_response))
                elif user.role == 'Student':
                    student = user.student
                    student_division = StudentDivision.objects.get(student=student)
                    branch = student.branch

                    student_response = {
                        'user_type': 'Student',
                        'year': student_division.division.year.year,
                        'branch': branch,
                        'division': student_division.division.division,
                        'name': user.student.first_name
                    }

                    return HttpResponse(str(student_response))

            else:
                return HttpResponse('sdfgvbhn')

        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)

            return HttpResponse(str(response))
    else:
        return HttpResponse(str('Not POst'))
