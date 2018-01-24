# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse

from General.models import CollegeExtraDetail, Shift, StudentDivision, CollegeYear, BranchSubject, Semester, \
    FacultySubject
from Registration.models import Student, Branch, Faculty, Subject
from UserModel.models import User
from .forms import StudentForm, FacultyForm, SubjectForm, FacultySubjectForm
from Configuration.stateConf import states


def view_subjects(request):
    subjects = BranchSubject.objects.filter(branch=Branch.objects.get(branch='Computer'))
    return render(request, 'view_subjects.html', {'subjects': subjects})


def register_faculty_subject(request):
    if request.method == 'POST':
        form = FacultySubjectForm(request.POST)
        if form.is_valid():
            faculty = Faculty.objects.get(pk=form.cleaned_data.get('faculty'))
            subject = Subject.objects.get(pk=form.cleaned_data.get('subject'))
            division = CollegeExtraDetail.objects.get(pk=form.cleaned_data.get('division'))

            if FacultySubject.objects.filter(faculty=faculty,
                                             subject=subject,
                                             division=division):
                return render(request, 'register_faculty_subject.html', {'form': FacultySubjectForm,
                                                                         'info': 'Binding Exists!'})

            else:
                faculty_subject = FacultySubject.objects.create(faculty=faculty,
                                                                subject=subject,
                                                                division=division)
                faculty_subject.save()
            return render(request, 'register_faculty_subject.html', {'form': FacultySubjectForm,
                                                                     'success': 'Successfully Bound'})
    elif request.method == 'GET':
        return render(request, 'register_faculty_subject.html', {'form': FacultySubjectForm})


def register_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            new_user = User.objects.create_user(username=student.gr_number,
                                                email=form.cleaned_data.get('email'),
                                                role='Student')
            new_user.save()
            division = form.cleaned_data.get('division')
            shift = form.cleaned_data.get('shift')
            branch = form.cleaned_data.get('branch')
            year = form.cleaned_data.get('year')

            student.user = new_user

            student.save()


            branch_obj = Branch.objects.get(branch=branch)
            college_year_obj = CollegeYear.objects.get(year=year)
            shift_obj = Shift.objects.get(shift=shift)
            new_student_division = StudentDivision(student=student,
                                                   division=CollegeExtraDetail.objects.get(branch=branch_obj,
                                                                                           year=college_year_obj,
                                                                                           division=division,
                                                                                           shift=shift_obj))
            new_student_division.save()
            request.session['user_id'] = student.pk
            return HttpResponseRedirect('/register/student/success/')
            # return HttpResponse(form.errors)
        else:
            print(form.errors)
            # return HttpResponse(form.errors)
        return render(request, "register_student.html", {'form': form})
    else:
        form = StudentForm(initial={'handicapped': False})
        return render(request, "register_student.html", {'form': form})


def register_faculty(request):
    if request.method == "POST":
        form = FacultyForm(request.POST, request.FILES)

        if form.is_valid():
            faculty = form.save(commit=False)
            if (request.POST.get('initials')) == '':
                if form.cleaned_data.get('middle_name') is None:
                    initials = str(form.cleaned_data.get('first_name'))[0] + str(form.cleaned_data.get('last_name'))[0]
                else:
                    initials = str(form.cleaned_data.get('first_name'))[0] + str(form.cleaned_data.get('middle_name'))[
                        0] + str(form.cleaned_data.get('last_name'))[0]

                initials = initials.upper()
                faculty.initials = initials
            new_user = User.objects.create_user(first_name=form.cleaned_data.get('first_name'),
                                                last_name=form.cleaned_data.get('last_name'),
                                                username=faculty.faculty_code,
                                                email=form.cleaned_data.get('email'))
            new_user.save()

            request.session['user_id'] = faculty.pk
            faculty.user = new_user
            faculty.save()
            return HttpResponseRedirect('/register/faculty/success/')
            # return HttpResponse(form.errors)
        else:
            return HttpResponse(form.errors)
    else:
        form = FacultyForm(initial={'handicapped': False})

    return render(request, "register_faculty.html", {'form': form})


def get_states(request):
    return HttpResponse(states)


def success_student(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        rpassword = request.POST.get('rpassword')
        if password == rpassword:
            user_id = request.session.get('user_id')
            student = Student.objects.get(pk=user_id)
            user = User.objects.get(username=student.gr_number)
            user.role = 'Student'
            user.set_password(password)
            user.save()
            request.session.flush()
            # student.save()
            return HttpResponseRedirect('/login/')
    else:
        user_id = request.session.get('user_id')
        student = Student.objects.get(pk=user_id)
        gr_number = student.gr_number
        return render(request, 'success.html', {
            'id': gr_number
        })


def success_faculty(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        rpassword = request.POST.get('rpassword')
        if password == rpassword:
            user_id = request.session.get('user_id')
            faculty = Faculty.objects.get(pk=user_id)
            user = User.objects.get(username=faculty.faculty_code)
            user.role = 'Faculty'
            user.set_password(password)
            user.save()
            request.session.flush()
            return HttpResponseRedirect('/login/')
        # else:
        #     return render(request, 'success.html', {
        #         'id': user.student.gr_number
        #     })

    else:
        user_id = request.session.get('user_id')
        faculty = Faculty.objects.get(pk=user_id)
        faculty_code = faculty.faculty_code
        return render(request, 'success.html', {
            'id': faculty_code
        })


def test(request):
    return render(request, 'online_test.html')


def get_division(request):
    branch = request.POST.get('branch')
    division_list = CollegeExtraDetail.objects.filter(branch=Branch.objects.get(branch=branch)).values_list('division',
                                                                                                            flat=True)
    return HttpResponse(division_list)


def get_shift(request):
    branch = request.POST.get('branch')
    shift = request.POST.get('shift')
    division_list = CollegeExtraDetail.objects.filter(shift=Shift.objects.get(shift=shift),
                                                      branch=Branch.objects.get(branch=branch)).values_list('division',
                                                                                                            flat=True)
    return HttpResponse(division_list)


def register_subject(request):
    if request.method == 'POST':

        subject_form = SubjectForm(request.POST)

        if subject_form.is_valid():
            subject_obj = subject_form.save()
            branch_object = Branch.objects.get(branch=subject_form.cleaned_data.get('branch'))
            year_obj = CollegeYear.objects.get(year=subject_form.cleaned_data.get('year'))
            semester_obj = Semester.objects.get(semester=subject_form.cleaned_data.get('semester'))
            # subject_obj = Subject.objects.get(code=subject_form.cleaned_data.get('code'))
            branch_subject = BranchSubject(branch=branch_object, year=year_obj,
                                           semester=semester_obj, subject=subject_obj)
            branch_subject.save()

            return render(request, 'test_register_subject.html',
                          {'success': subject_obj.short_form + ' is Successfully registered',
                           'form': SubjectForm()})

        else:
            return HttpResponse('error : ' + str(subject_form.errors))

    else:
        subject_form = SubjectForm()
    return render(request, 'test_register_subject.html',
                  {'form': subject_form})
