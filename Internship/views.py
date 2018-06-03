import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from General.models import StudentInternship
from Internship.forms import StudentInternshipForm
from Internship.models import Internship
from Registration.models import Branch
from Registration.views import has_role


def apply(request):
    user = request.user
    if not user.is_anonymous:
        if has_role(user, 'student'):
            if request.method == 'GET':
                return render(request, 'apply.html',
                              context={'form': StudentInternshipForm})
            elif request.method == 'POST':
                student_internship_form_obj = StudentInternshipForm(request.POST)
                if student_internship_form_obj.is_valid():
                    student_internship_obj = student_internship_form_obj.save(commit=False)
                    intership_pk = request.POST.get('internship')
                    internship_obj = Internship.objects.get(pk=intership_pk)
                    student_internship_obj.application_date = datetime.date.today()
                    student_internship_obj.start_date = student_internship_form_obj.cleaned_data['start_date']
                    student_internship_obj.end_date = student_internship_form_obj.cleaned_data['end_date']
                    student_internship_obj.student = user.student
                    student_internship_obj.internship = internship_obj
                    student_internship_obj.save()

                    return render(request, 'apply.html',
                                  context={'form': StudentInternshipForm,
                                           'success': 'Submitted successfully. You will get notification if application is accepted.'})
                else:
                    return render(request, 'apply.html',
                                  context={'form': student_internship_form_obj,
                                           'error': 'Form not valid. ' + str(student_internship_form_obj.errors)})

        else:
            return HttpResponse('faculty not allowed')


    else:
        return redirect('/login/')


def review(request):
    user = request.user
    if not user.is_anonymous:
        if has_role(user, 'faculty'):
            if request.method == 'GET':
                branch_obj = Branch.objects.get(branch='Computer')
                all_student_internship_objs = StudentInternship.objects.filter(internship__branch=branch_obj,
                                                                               is_active=True)
                all_student_internship_objs_not_accepted = all_student_internship_objs.filter(is_accepted=False)
                all_student_internship_objs_accepted = all_student_internship_objs.filter(is_accepted=True)

                return render(request, 'internship_list.html',
                              {'student_internships_not_accepted': all_student_internship_objs_not_accepted,
                               'student_internships_accepted': all_student_internship_objs_accepted})
            elif request.POST.get('review_button'):
                student_internship_pk = request.POST.get('review_button')
                student_internship_obj = StudentInternship.objects.get(pk=student_internship_pk)

                return render(request, 'review_internship.html',
                              {'student_internship': student_internship_obj})
            elif request.POST.get('accept_button'):
                student_internship_pk = request.POST.get('accept_button')
                remarks = request.POST.get('remarks')
                student_internship_obj = StudentInternship.objects.get(pk=student_internship_pk)
                student_internship_obj.is_reviewed = True
                student_internship_obj.is_accepted = True
                student_internship_obj.remarks = remarks
                student_internship_obj.save()

                return render(request, 'review_internship.html',
                              {'student_internship': student_internship_obj})
            elif request.POST.get('reject_button'):
                student_internship_pk = request.POST.get('reject_button')
                remarks = request.POST.get('remarks')
                student_internship_obj = StudentInternship.objects.get(pk=student_internship_pk)
                student_internship_obj.is_reviewed = True
                student_internship_obj.is_accepted = False
                student_internship_obj.remarks = remarks
                student_internship_obj.save()

                return render(request, 'review_internship.html',
                              {'student_internship': student_internship_obj})



        else:
            return HttpResponse('student not allowed')


    else:
        return redirect('/login/')


def status(request):
    user = request.user
    if not user.is_anonymous:
        if has_role(user, 'student'):
            student = user.student
            if request.method == 'GET':
                student_internship_objs = StudentInternship.objects.filter(student=student)
                return render(request, 'application_status.html',
                              {'application_list': True,
                               'student_internship_objs': student_internship_objs})
            elif request.POST.get('reapply_button'):
                student_internship_obj = StudentInternship.objects.get(pk=request.POST.get('reapply_button'))
                return render(request, 'apply.html',
                              {'form': StudentInternshipForm(instance=student_internship_obj)})

        else:
            return HttpResponse('faculty not allowed')


    else:
        return redirect('/login/')