from __future__ import unicode_literals

import json

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from General.models import StudentDivision
from Registration.models import Faculty, Student, Branch
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
                    faculty_response = {
                        'user_type': 'Faculty',
                        'initials': user.faculty.initials,
                        'name': user.faculty.first_name
                    }
                    return HttpResponse(str(faculty_response))
                elif user.role == 'Student':
                    student = user.student
                    student_division = StudentDivision.objects.get(student=student)
                    branch = student.branch
                    branch_obj = Branch.objects.get(branch=branch)

                    student_response = {
                        'user_type': 'Student',
                        'year': student_division.division.year.year,
                        'branch': student_division.division.branch.branch,
                        'division': student_division.division.division,
                        'name': user.student.first_name
                    }
                    return HttpResponse(str(student_response))
            else:
                return HttpResponse(str(response))

        except:
            return HttpResponse(str(response))
    return HttpResponse(str(response))
