from __future__ import unicode_literals

import hashlib
import json

from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt

from EnterpriseResourcePlanning import conf
from EnterpriseResourcePlanning.conf import email_sending_service_enabled
from General.models import StudentDetail, Division
from Registration.models import Faculty, Student, Branch
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
            print(request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            print(user)
            if user:

                user = User.objects.get(username=username)
                # print(user.role)
                if user.role == 'Faculty':
                    faculty = user.faculty
                    faculty_response = {
                        'user_type': 'Faculty',
                        'initials': user.faculty.initials,
                        'name': user.faculty.first_name + user.faculty.last_name
                    }

                    # return HttpResponse(str(faculty_response))
                    all_divisions = Division.objects.filter().all()

                    attendance_list = {}

                    for each_division in all_divisions:

                        all_student = [each.student for each in
                                       StudentDetail.objects.filter(batch__division=each_division).distinct()]

                        year = each_division.year.year

                        division = each_division.division
                        branch = each_division.branch.branch

                        if year in attendance_list:

                            if branch in attendance_list[year]:
                                if division in attendance_list[year][branch]:
                                    pass
                                else:
                                    attendance_list[year][branch][division] = {}
                            else:
                                attendance_list[year][branch] = {}
                                attendance_list[year][branch][division] = {}

                        else:
                            attendance_list[year] = {}
                            attendance_list[year][branch] = {}
                            attendance_list[year][branch][division] = {}
                        # attendance_list[year][branch][division] = sorted([
                        #     StudentRollNumber.objects.get(student=each_student.student, is_active=True) for
                        #     each_student in all_student])

                        for each_student in all_student:

                            roll_number = StudentDetail.objects.filter(student=each_student,
                                                                       is_active=True)[0].roll_number

                            if 'all' in attendance_list[year][branch][division]:
                                attendance_list[year][branch][division]['all'].append(roll_number)
                            else:
                                attendance_list[year][branch][division]['all'] = []
                                attendance_list[year][branch][division]['all'].append(roll_number)
                            curr_batch = StudentDetail.objects.get(student=each_student).batch.batch_name
                            if curr_batch in attendance_list[year][branch][division]:
                                attendance_list[year][branch][division][curr_batch].append(roll_number)
                            else:
                                attendance_list[year][branch][division][curr_batch] = []
                                attendance_list[year][branch][division][curr_batch].append(roll_number)

                            # attendance_list[year][branch][division] = {}
                        #
                        # for each_student in all_student:
                        #     attendance_list[year][branch][division].appned(
                        #         StudentRollNumber.objects.get(student=each_student, is_active=True).roll_number)

                    faculty_response['attendance_list'] = attendance_list
                    print(HttpResponse(json.dumps(faculty_response)))
                    return HttpResponse(json.dumps(faculty_response))
                elif user.role == 'Student':
                    student = user.student
                    student_detail = StudentDetail.objects.get(student=student)
                    branch = student.branch

                    student_response = {
                        'user_type': 'Student',
                        'year': student_detail.batch.division.year.year,
                        'branch': branch,
                        'division': student_detail.batch.division.division,
                        'batch': student_detail.batch.batch_name,
                        'name': user.student.first_name + user.student.last_name
                    }

                    return HttpResponse(str(student_response))

            else:
                return HttpResponse(str(response))

        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)

            return HttpResponse(str(message))
    else:
        return render(request, 'login.html')


def generate_activation_key():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    secret_key = get_random_string(20, chars)

    return hashlib.sha256((secret_key).encode('utf-8')).hexdigest()
