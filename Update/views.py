from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from UserModel.models import User
from .forms import StudentUpdateForm, FacultyUpdateForm
from Registration.models import Student


def update(request):
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
                    return HttpResponseRedirect('/dashboard/')
                else:
                    print('form not valid')
                    print(form.errors)
                    return render(request, 'update.html', {
                        'form': form,
                    })

            elif user.role=='Faculty':
                form = FacultyUpdateForm(request.POST or None, request.FILES or None, instance=user.faculty)

                faculty = user.faculty
                print(request.FILES)
                print(user.faculty.first_name)

                if form.is_valid():
                    print('form valid')

                    faculty_obj = form.save(commit=False)
                    faculty_obj.user = user
                    faculty_obj.save()
                    return render(request, 'update.html', {
                        'form': form,
                        'success': 'Successfully updated.'
                    })
                else:
                    print('form not valid')
                    #print validation error
                    print(form.errors)
                    return render(request, 'update.html', {
                        'form': form,
                        'error': 'Updating failed.'
                    })

        else:
            print('got user id', user)
            if user.role=='Faculty':
                print('in update faculty')
                obj = user.faculty
                print(user.email,"sdfevsrdvsdvrsdbvfbrff")
                form = FacultyUpdateForm(instance=obj)

            elif user.role=='Student':
                print('in update student')
                obj = user.student
                form = StudentUpdateForm(instance=obj)
            else:
                return HttpResponse("User has no role")

            return render(request, 'update.html', {
                'form': form,
            })
    else:
        print('Redirecting to login')
        return HttpResponseRedirect('/login/')


def update_role(request):
    if request.method == 'GET':
        return render(request, 'update_role.html', context={'facultys'})
    return None