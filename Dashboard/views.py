from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

from Registration.forms import StudentForm, FacultyForm
from Registration.models import Student

# Student dashboard
from Update.forms import StudentUpdateForm, FacultyUpdateForm
from UserModel.models import User


# def student(request):
#     user = request.user
#     # If user exists in session (i.e. logged in)
#     if not user.is_anonymous:
#         student_obj = user.student
#         form = StudentForm(instance=student_obj)
#         return render(request, 'dashboard.html', {
#             'form': form,
#             'first_name': user.first_name,
#             'last_name': user.last_name,
#
#         })
#     else:
#         return HttpResponseRedirect('/login/')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def show_dashboard(request):
    user = request.user
    # If user exists in session (i.e. logged in)
    if not user.is_anonymous:
        if user.role == 'Student':
            student_obj = user.student
            form = StudentForm(instance=student_obj)
            return render(request, 'dashboard_student.html', {
                'form': form,
            })
        elif user.role == 'Faculty':
            faculty_obj = user.faculty
            form = FacultyForm(instance=faculty_obj)
            return render(request, 'dashboard_faculty.html', {
                'form': form,
            })
    else:
        print('not logged in')
        return redirect('/login/')


def view_profile(request):
    user = request.user
    if not user.is_anonymous:
        if request.method == 'POST':
            if user.role == 'Student':
                form = StudentUpdateForm(request.POST, request.FILES, instance=user.student)
                print(request.FILES)
                print(user.student)
                if form.is_valid():
                    print('form valid')
                    student_obj = form.save(commit=False)
                    student_obj.user = user
                    student_obj.save()
                    return HttpResponseRedirect('/dashboard/')
                else:
                    print('form not valid')
                    print(form.errors)
                    return render(request, 'profile_student.html', {
                        'form': form,
                    })

            elif user.role == 'Faculty':
                form = FacultyUpdateForm(request.POST, request.FILES, instance=user.faculty)
                print(request.FILES)
                print(user.faculty)
                if form.is_valid():
                    print('form valid')
                    faculty_obj = form.save(commit=False)
                    faculty_obj.user = user
                    faculty_obj.save()
                    return HttpResponseRedirect('/dashboard/')
                else:
                    print('form not valid')
                    print(form.errors)
                    return render(request, 'profile_faculty.html', {
                        'form': form,
                    })

        else:
            print('got user id', user)
            if user.role == 'Faculty':
                print('in update faculty')
                obj = user.faculty
                form = FacultyUpdateForm(instance=obj)
                return render(request, 'profile_faculty.html', {
                    'form': form,
                })

            elif user.role == 'Student':
                print('in update student')
                obj = user.student
                form = StudentUpdateForm(instance=obj)
                return render(request, 'profile_student.html', {
                    'form': form,
                })

            else:
                return HttpResponse("User has no role")


    else:
        print('Redirecting to login')
        return HttpResponseRedirect('/login/')


def view_research(request):
    return render(request, 'view_research.html', {})