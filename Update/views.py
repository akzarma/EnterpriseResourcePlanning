from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from UserModel.models import User, RoleManager
from .forms import StudentUpdateForm, FacultyUpdateForm
from Registration.models import Student
from Exam.models import ExamMaster


def update(request):
    user = request.user
    if not user.is_anonymous:
        is_faculty = RoleManager.objects.filter(user=user, role__role='faculty')
        is_student = RoleManager.objects.filter(user=user, role__role='student')
        if request.method == 'POST':
            if is_student:
                form = StudentUpdateForm(request.POST or None, request.FILES or None, instance=user.student)
                if form.is_valid():
                    student_obj = form.save(commit=False)
                    student_obj.user = user
                    student_obj.save()
                    return render(request, 'update_student.html', {
                        'form': form,
                        'success': 'Successfully updated.'
                    })
                else:
                    return render(request, 'update_faculty.html', {
                        'form': form,
                        'error': 'Updating failed.'
                    })

            elif is_faculty:
                form = FacultyUpdateForm(request.POST or None, request.FILES or None, instance=user.faculty)
                if form.is_valid():
                    faculty_obj = form.save(commit=False)
                    faculty_obj.user = user
                    faculty_obj.save()
                    return render(request, 'update_faculty.html', {
                        'form': form,
                        'success': 'Successfully updated.'
                    })
                else:
                    return render(request, 'update_faculty.html', {
                        'form': form,
                        'error': 'Updating failed.'
                    })

        else:
            if is_faculty:
                obj = user.faculty
                form = FacultyUpdateForm(instance=obj)
                return render(request, 'update_faculty.html', {
                    'form': form,
                })

            elif is_student:
                obj = user.student
                form = StudentUpdateForm(instance=obj)
                return render(request, 'update_student.html', {
                    'form': form,
                })
            else:
                return HttpResponse("User has no role")


    else:
        return HttpResponseRedirect('/login/')


def update_role(request):
    if request.method == 'GET':
        return render(request, 'update_role.html', context={'facultys'})
    return None


def update_exam_status(request):
    if request.method == "GET":
        data_set = ExamMaster.objects.all()

        return render(request, 'update_exam_status.html', {'dataset': data_set})
    elif request.method == "POST":
        id = request.POST.get('id')
        exam = ExamMaster.objects.get(pk=id)
        exam.is_active = not exam.is_active
        exam.save()
        data_set = ExamMaster.objects.all()

        return render(request, 'update_exam_status.html', {'dataset': data_set})
