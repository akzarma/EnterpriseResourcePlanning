from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render

from Registration.forms import StudentForm
from Registration.models import Student


# Student dashboard
from UserModel.models import User


def student(request):
    user = request.user
    # If user exists in session (i.e. logged in)
    print(user)
    if not user.is_anonymous:
        print('logged in')
        print(user)
        student_obj = user.student
        form = StudentForm(instance=student_obj)
        return render(request, 'dashboard.html', {
            'form': form,
            'first_name': user.first_name,
            'last_name': user.last_name,

        })
    else:
        print('not logged in')
        return HttpResponseRedirect('/login/')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def test_url(request):
    user = request.user
    # If user exists in session (i.e. logged in)
    print(user)
    if not user.is_anonymous:
        print('logged in')
        print(user)
        if user.role=='Student':
            student_obj = user.student
            form = StudentForm(instance=student_obj)
            return render(request, 'testdash.html', {
                'form': form,
            })
        elif user.role=='Faculty':
            faculty_obj = user.faculty
            form = StudentForm(instance=faculty_obj)
            return render(request, 'testdash.html', {
                'form': form,
            })
    else:
        print('not logged in')
        return HttpResponseRedirect('/login/')
