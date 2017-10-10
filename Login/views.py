from __future__ import unicode_literals

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from General.models import StudentDivision
from Registration.models import Faculty, Student
from UserModel.models import User
import json



def login_user(request):
    print("login user")
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/dashboard/student/')
        else:
            return HttpResponseRedirect('/login/')
    return render(request, 'login.html')


@csrf_exempt
def login_android(request):
    response = [{
                    'userType': 'null'
                    }]
    if request.method == 'POST':
        print(request.POST)
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)

            print(user.role)

            if user:

                user = User.objects.get(username=username)
                if user.role == 'Faculty':
                    faculty_response =[
                    {
                        'userType': 'Faculty'
                    }]
                    return HttpResponse(str(faculty_response[0]))
                elif user.role == 'Student':
                    student_division = StudentDivision.objects.get(student=user.student)

                    student_response = [{
                        'userType': 'Student',
                        'year': student_division.division.year.year,
                        'branch': student_division.division.branch.branch,
                        'division': student_division.division.division,
                    }]
                    return HttpResponse(str(student_response[0]))
            else:
                return HttpResponse(str(response[0]))
        except:

            return HttpResponse(str(response[0]))
    return HttpResponse(str(response[0]))
