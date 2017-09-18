# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse

from Registration.models import Student
from .forms import StudentForm, FacultyForm, SubjectForm
from Configuration.stateConf import states


def register_student(request):
    print("here")
    if request.method == "POST":
        print("Register student post")
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            print("Valid")
            student = form.save(commit=False)
            print(student.gr_number)
            new_user = User.objects.create_user(first_name=form.cleaned_data.get('first_name'),
                                                last_name=form.cleaned_data.get('last_name'),
                                                username=student.gr_number,
                                                email=form.cleaned_data.get('email'))
            print("email: ", new_user.email)
            new_user.save()
            print(new_user)
            student.user = new_user

            # student.first_name = student.first_name.title()
            # student.middle_name = student.middle_name.title()
            # student.last_name = student.last_name.title()
            # student.father_name = student.father_name.title()
            # student.mother_name = student.mother_name.title()
            # student.emergency_name = student.emergency_name.title()
            student.save()
            # print(student.pk)
            request.session['user_id'] = student.pk
            # print(request.session.get('user_id', 0))
            return HttpResponseRedirect('/register/student/success/')
            # return HttpResponse(form.errors)
        else:
            print(form.errors)
            # return HttpResponse(form.errors)
        return render(request, "register_student.html", {'form': form})
    else:
        print("Register student not POST")
        form = StudentForm(initial={'handicapped': False})
        return render(request, "register_student.html", {'form': form})


def register_faculty(request):
    if request.method == "POST":
        print("Register faculty post")
        form = FacultyForm(request.POST, request.FILES)
        if form.is_valid():
            print("Valid")
            form.save()
            return HttpResponseRedirect('/register/faculty/')
            # return HttpResponse(form.errors)
        else:
            print(form.errors)
            # return HttpResponse(form.errors)
        return render(request, "register_faculty.html", {'form': form})
    else:
        print("Register faculty not POST")
        form = FacultyForm(initial={'handicapped': False})

    return render(request, "register_faculty.html", {'form': form})


def register_subject(request):
    if request.method == "POST":
        print("Register subject post")
        form = SubjectForm(request.POST, request.FILES)
        if form.is_valid():
            print("Valid")
            form.save()
            return HttpResponseRedirect('/register/subject/')
            # return HttpResponse(form.errors)
        else:
            print(form.errors)
            # return HttpResponse(form.errors)
        return render(request, "register_subject.html", {'form': form})
    else:
        print("Register subject not POST")
        form = SubjectForm()

    return render(request, "register_subject.html", {'form': form})


def get_states(request):
    print(states)
    return HttpResponse(states)


def success_student(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        rpassword = request.POST.get('rpassword')
        if password == rpassword:
            user_id = request.session.get('user_id')
            student = Student.objects.get(pk=user_id)
            user = User.objects.get(username=student.gr_number)
            print(password)
            user.set_password(password)
            user.save()
            request.session.flush()
            # student.save()
            print('password saved')
            return HttpResponseRedirect('/login/')
    else:
        user_id = request.session.get('user_id')
        student = Student.objects.get(pk=user_id)
        gr_number = student.gr_number
        return render(request, 'success.html', {
            'gr_number': gr_number
        })


def test(request):
    return render(request, 'online_test.html')


def get_division(request, branch):
    return None
