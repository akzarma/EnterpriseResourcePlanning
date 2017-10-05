from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .forms import StudentUpdateForm, FacultyUpdateForm
from Registration.models import Student


def update_student(request):
    user = request.user
    if not user.is_anonymous:
        if request.method == 'POST':
            if user.role=='Student':
                form = StudentUpdateForm(request.POST, request.FILES, instance=user.student)
                print(request.FILES)
                print(user.student)
                if form.is_valid():
                    print('form valid')
                    student_obj = form.save(commit=False)
                    student_obj.user = user
                    student_obj.save()
                    return HttpResponseRedirect('/dashboard/student/')
                else:
                    print('form not valid')
                    print(form.errors)
                    return render(request, 'update_student.html', {
                        'form': form,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    })

            elif user.role=='Faculty':
                form = StudentUpdateForm(request.POST, request.FILES, instance=user.faculty)
                print(request.FILES)
                print(user.faculty)
                if form.is_valid():
                    print('form valid')
                    faculty_obj = form.save(commit=False)
                    faculty_obj.user = user
                    faculty_obj.save()
                    return HttpResponseRedirect('/dashboard/student/')
                else:
                    print('form not valid')
                    print(form.errors)
                    return render(request, 'update_student.html', {
                        'form': form,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    })

        else:
            print('got user id', user)
            if user.role=='Faculty':
                obj = user.faculty
                form = FacultyUpdateForm(instance=obj)
            elif user.role=='Student':
                obj = user.student
                form = StudentUpdateForm(instance=obj)
            else:
                return HttpResponse("User has no role")

            return render(request, 'update_student.html', {
                'form': form,
                'first_name': user.first_name,
                'last_name': user.last_name,
            })
    else:
        print('Redirecting to login')
        return HttpResponseRedirect('/login/')


def update_role(request):
    if request.method == 'GET':
        return render(request, 'update_role.html', context={'facultys'})
    return None