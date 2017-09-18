from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .forms import StudentUpdateForm
from Registration.models import Student


def update_student(request):
    user = request.user
    if not user.is_anonymous:
        if request.method == 'POST':
            form = StudentUpdateForm(request.POST, request.FILES, instance=user.studentdetails)
            print(request.FILES)
            print(user.studentdetails)
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
        else:
            print('got user id')
            student_obj = user.studentdetails
            form = StudentUpdateForm(instance=student_obj)
            return render(request, 'update_student.html', {
                'form': form,
                'first_name': user.first_name,
                'last_name': user.last_name,
            })
    else:
        print('Redirecting to login')
        return HttpResponseRedirect('/login/')
