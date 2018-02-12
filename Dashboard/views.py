import json
from itertools import chain

from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

from General.models import Batch, StudentDivision
from Registration.forms import StudentForm, FacultyForm
from Registration.models import Student
import datetime
# Student dashboard
from Research.models import Paper
from Timetable.models import Timetable, DateTimetable
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
        date_range = [datetime.date.today() + datetime.timedelta(n) for n in [-1, 0, 1]]
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        if user.role == 'Student':
            student = user.student
            college_extra_detail = StudentDivision.objects.get(student=student, is_active=True).division
            total_attendance = student.totalattendance_set.all()
            timetable = sorted(
                DateTimetable.objects.filter(date__in=date_range, original__division=college_extra_detail),
                key=lambda x: (x.date, x.original.time.starting_time))

            attendance = {}
            attended = 0
            total = 0

            for each in total_attendance:
                total += each.total_lectures
                attended += each.attended_lectures
                if each.total_lectures is not 0:
                    subject_attendance = round(100* each.attended_lectures/each.total_lectures,2)
                else:
                    subject_attendance =  0
                attendance[each.subject.short_form] = {
                    'total': each.total_lectures,
                    'attended': each.attended_lectures,
                    'attendance': subject_attendance ,
                }
            total_percent = round(100 * attended / total, 2)

            return render(request, 'dashboard_student.html', {
                'timetable': timetable,
                'date_range': date_range,
                'days': days,
                'total_attendance': total_percent,
                'attendance': attendance,
            })
        elif user.role == 'Faculty':
            faculty = user.faculty
            timetable = sorted(
                DateTimetable.objects.filter(date__in=date_range, original__faculty=faculty),
                key=lambda x: (x.date, x.original.time.starting_time))
            return render(request, 'dashboard_faculty.html', {
                'timetable': timetable,
                'date_range': date_range,
                'days': days,
            })
        else:
            logout_user(request)
            return redirect('/login/')
    else:
        return redirect('/login/')


def view_profile(request):
    user = request.user
    if not user.is_anonymous:
        if request.method == 'POST':
            if user.role == 'Student':
                form = StudentUpdateForm(request.POST, request.FILES, instance=user.student)
                if form.is_valid():
                    student_obj = form.save(commit=False)
                    student_obj.user = user
                    student_obj.save()
                    return HttpResponseRedirect('/dashboard/')
                else:
                    return render(request, 'profile_student.html', {
                        'form': form,
                    })

            elif user.role == 'Faculty':
                form = FacultyUpdateForm(request.POST, request.FILES, instance=user.faculty)
                if form.is_valid():
                    faculty_obj = form.save(commit=False)
                    faculty_obj.user = user
                    faculty_obj.save()
                    return HttpResponseRedirect('/dashboard/')
                else:
                    return render(request, 'profile_faculty.html', {
                        'form': form,
                    })

        else:
            if user.role == 'Faculty':
                obj = user.faculty
                form = FacultyUpdateForm(instance=obj)
                return render(request, 'profile_faculty.html', {
                    'form': form,
                })

            elif user.role == 'Student':
                obj = user.student
                form = StudentUpdateForm(instance=obj)
                return render(request, 'profile_student.html', {
                    'form': form,
                })

            else:
                return HttpResponse("User has no role")


    else:
        return HttpResponseRedirect('/login/')


def list_research(request):
    user = request.user
    all_papers = Paper.objects.filter(faculty=user.faculty)
    return render(request, 'list_research.html', {'all_papers': all_papers})
