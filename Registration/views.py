# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime, json

# from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.utils.dateparse import parse_date

from EnterpriseResourcePlanning import conf
from EnterpriseResourcePlanning.conf import email_sending_service_enabled
from General.models import Division, Shift, StudentDetail, CollegeYear, BranchSubject, Semester, \
    FacultySubject, Batch, YearBranch, StudentSubject, YearSemester, Schedulable, ElectiveDivision, ElectiveBatch
from General.views import notify_users
from Login.views import generate_activation_key
from Registration.models import Student, Branch, Faculty, Subject, ElectiveSubject
from Roles.models import User, RoleManager, RoleMaster
from Timetable.models import Room
from .forms import StudentForm, FacultyForm, SubjectForm, FacultySubjectForm, gr_roll_dict, DateScheduleForm, \
    YearBranchSemForm
from Configuration.stateConf import states


def has_role(user: User, role: str):
    role_obj = RoleMaster.objects.get(role=role, is_active=True)
    if RoleManager.objects.filter(user=user, role=role_obj, is_active=True).exists():
        return True
    else:
        return False


def view_subjects(request):
    subjects = BranchSubject.objects.filter(year_branch__branch=Branch.objects.get(branch='Computer'))
    return render(request, 'view_subjects.html', {'subjects': subjects})


def register_faculty_subject(request):
    class_active = "register"
    elective_list = list(Subject.objects.filter(is_elective_group=True).values_list('short_form', flat=True))
    if request.method == 'POST':
        form = FacultySubjectForm(request.POST)
        if form.is_valid():
            faculty = Faculty.objects.get(pk=form.cleaned_data.get('faculty'))
            subject = Subject.objects.get(pk=form.cleaned_data.get('subject'))
            if subject.is_elective_group == True:
                elective_subject = form.cleaned_data.get('elective_subject')
                elective_division = form.cleaned_data.get('elective_division')
                faculty_subject_obj = FacultySubject.objects.filter(faculty=faculty,
                                                                    subject=subject,
                                                                    elective_subject=elective_subject,
                                                                    elective_division=elective_division)

            else:
                division = Division.objects.get(pk=form.cleaned_data.get('division'))

                faculty_subject_obj = FacultySubject.objects.filter(faculty=faculty,
                                                                    subject=subject,
                                                                    division=division)

            if faculty_subject_obj:
                return render(request, 'register_faculty_subject.html', {
                    'class_active': class_active,
                    'form': FacultySubjectForm,
                    'elective_list': elective_list,
                    'info': 'Binding Exists!'})

            else:
                faculty_subject = FacultySubject.objects.create(faculty=faculty,
                                                                subject=subject,
                                                                division=division) if subject.is_elective_group == False else FacultySubject.objects.create(
                    faculty=faculty,
                    subject=subject,
                    elective_subject=elective_subject,
                    elective_division=elective_division)
                faculty_subject.save()
            return render(request, 'register_faculty_subject.html', {
                'class_active': class_active,
                'form': FacultySubjectForm, 'elective_list': json.dumps(elective_list),
                'success': 'Successfully Bound'
            })
    elif request.method == 'GET':
        return render(request, 'register_faculty_subject.html', {
            'class_active': class_active,
            'form': FacultySubjectForm, 'elective_list': json.dumps(elective_list)
        })


def auto_register_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        i = 1
        while (i < 46):
            if form.is_valid():
                student = 0
                try:
                    student = form.save(commit=False)
                    student.key = generate_activation_key()
                    curr_gr_number = 'ENTC' + str(i)
                    student.gr_number = curr_gr_number
                    student.first_name = 'Akz' + str(i)
                    new_user = User.objects.create_user(username=student.gr_number,
                                                        first_name='Akz' + str(i),
                                                        last_name=form.cleaned_data.get('last_name'),
                                                        email=form.cleaned_data.get('email'))
                    new_user.save()
                    # division = form.cleaned_data.get('division')
                    shift = form.cleaned_data.get('shift')
                    branch = form.cleaned_data.get('branch')
                    year = form.cleaned_data.get('year')
                    # batch = form.cleaned_data.get('batch')
                    if 1 <= i <= 15:
                        batch = 'A1'
                        division = 'A'
                    elif 15 < i <= 30:
                        batch = 'B1'
                        division = 'B'
                    else:
                        batch = 'C1'
                        division = 'C'
                        shift = '2'

                    student.user = new_user

                    student.save()

                    roll_number = str(i)
                    if year == 'FE':
                        branch_obj = Branch.objects.get(branch='E&AS')
                    else:
                        branch_obj = Branch.objects.get(branch=branch)
                    year_obj = CollegeYear.objects.get(year=year)
                    year_branch_obj = YearBranch.objects.get(branch=branch_obj, year=year_obj, is_active=True)
                    shift_obj = Shift.objects.get(year_branch=year_branch_obj, shift=shift)
                    division_obj = Division.objects.get_or_create(year_branch=year_branch_obj,
                                                                  division=division, shift=shift_obj)[0]
                    batch_obj = Batch.objects.get_or_create(division=division_obj, batch_name=batch)[0]
                    sem_obj = Semester.objects.get(semester=2, is_active=True)
                    StudentDetail.objects.get_or_create(student=student, batch=batch_obj, roll_number=roll_number,
                                                        semester=sem_obj)

                    # college_year_obj = CollegeYear.objects.get(year=year)
                    # shift_obj = Shift.objects.get(shift=shift)
                    # new_student_division = StudentDetail(student=student,
                    #                                      division=CollegeExtraDetail.objects.get(branch=branch_obj,
                    #                                                                                year=college_year_obj,
                    #                                                                                division=division,
                    #                                                                                shift=shift_obj))
                    # StudentRollNumber.objects.create(student=student, roll_number=[gr_roll_dict[i] for i in gr_roll_dict if i==student.gr_number][0])
                    # new_student_division.save()
                    request.session['user_id'] = student.pk
                    # user_id = request.session.get('user_id')
                    # student = Student.objects.get(pk=user_id)
                    user = User.objects.get(username=student.gr_number)
                    role = RoleMaster.objects.get(role='student')
                    RoleManager.objects.create(user=user, role=role, start_date=datetime.date.today())
                    # user.role = 'Student'
                    user.set_password('test')
                    user.save()
                    request.session.flush()
                    print('done ' + student.gr_number)
                    # return HttpResponse(form.errors)
                except Exception as e:
                    if not student == 0:
                        StudentDetail.objects.filter(student=student).delete()
                        Student.objects.filter(pk=student.pk).delete()
                        User.objects.filter(pk=student.pk).delete()
                    form = StudentForm(initial={'handicapped': False})
                    return render(request, "register_student.html", {'form': form,
                                                                     'error': e})
            else:
                print(form.errors)
                # return HttpResponse(form.errors)
            i += 1

        return render(request, "register_student.html", {'form': form})
    else:
        form = StudentForm(initial={'handicapped': False})
        return render(request, "register_student.html", {'form': form})


def register_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = 0
            try:
                student = form.save(commit=False)
                student.key = generate_activation_key()
                new_user = User.objects.create_user(username=student.gr_number,
                                                    first_name=form.cleaned_data.get('first_name'),
                                                    last_name=form.cleaned_data.get('last_name'),
                                                    email=form.cleaned_data.get('email'))
                new_user.save()
                division = form.cleaned_data.get('division')
                shift = form.cleaned_data.get('shift')
                branch = form.cleaned_data.get('branch')
                year = form.cleaned_data.get('year')
                batch = form.cleaned_data.get('batch')
                batch = "".join(batch.split()).upper()
                division = "".join(division).upper()

                student.user = new_user

                student.save()

                roll_number = gr_roll_dict[student.gr_number]
                if year == 'FE':
                    branch_obj = Branch.objects.get(branch='E&AS')
                else:
                    branch_obj = Branch.objects.get(branch=branch)
                year_obj = CollegeYear.objects.get(year=year)
                year_branch_obj = YearBranch.objects.get(branch=branch_obj, year=year_obj, is_active=True)
                shift_obj = Shift.objects.get(year_branch=year_branch_obj, shift=shift)
                division_obj = Division.objects.get_or_create(year_branch=year_branch_obj,
                                                              division=division, shift=shift_obj)[0]
                batch_obj = Batch.objects.get_or_create(division=division_obj, batch_name=batch)[0]
                sem_obj = Semester.objects.get(semester=1, is_active=True)
                StudentDetail.objects.get_or_create(student=student, batch=batch_obj, roll_number=roll_number,
                                                    semester=sem_obj)

                # college_year_obj = CollegeYear.objects.get(year=year)
                # shift_obj = Shift.objects.get(shift=shift)
                # new_student_division = StudentDetail(student=student,
                #                                      division=CollegeExtraDetail.objects.get(branch=branch_obj,
                #                                                                                year=college_year_obj,
                #                                                                                division=division,
                #                                                                                shift=shift_obj))
                # StudentRollNumber.objects.create(student=student, roll_number=[gr_roll_dict[i] for i in gr_roll_dict if i==student.gr_number][0])
                # new_student_division.save()
                request.session['user_id'] = student.pk
                return HttpResponseRedirect('/register/student/success/')
                # return HttpResponse(form.errors)
            except Exception as e:
                if not student == 0:
                    StudentDetail.objects.filter(student=student).delete()
                    Student.objects.filter(pk=student.pk).delete()
                    User.objects.filter(pk=student.pk).delete()
                form = StudentForm(initial={'handicapped': False})
                return render(request, "register_student.html", {'form': form,
                                                                 'error': e})
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
            role = RoleMaster.objects.get(role='student')
            RoleManager.objects.create(user=user, role=role, start_date=datetime.date.today())
            # user.role = 'Student'
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
                'id': gr_number,
                'error': 'Passwords didn\'t match.'
            })
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
            role = RoleMaster.objects.get(role='faculty')
            RoleManager.objects.create(user=user, role=role, start_date=datetime.date.today())
            # user.role = 'Faculty'
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
    division_list = Division.objects.filter(year_branch__branch=Branch.objects.get(branch=branch)).values_list(
        'division',
        flat=True)
    return HttpResponse(division_list)


def get_shift(request):
    branch = request.POST.get('branch')
    shift = request.POST.get('shift')
    division_list = Division.objects.filter(shift=Shift.objects.get(shift=shift),
                                            branch=Branch.objects.get(branch=branch)).values_list('division',
                                                                                                  flat=True)
    return HttpResponse(division_list)


def register_subject(request):
    user = request.user
    class_active = "register"
    if not user.is_anonymous:

        if request.method == 'POST' and request.POST.get('register_subject'):
            subject_form = SubjectForm(request.POST)
            if subject_form.is_valid():
                branch_object = Branch.objects.get(branch=subject_form.cleaned_data.get('branch'))
                year_obj = CollegeYear.objects.get(year=subject_form.cleaned_data.get('year'))
                semester_obj = Semester.objects.get(semester=subject_form.cleaned_data.get('semester'))
                year_branch_obj = YearBranch.objects.get(branch=branch_object, year=year_obj, is_active=True)
                if request.POST.get('is_elective_group'):
                    subject_form.is_elective_group = True
                    subject_obj = subject_form.save(commit=False)
                    no_of_elective = int(request.POST.get('no_of_elective'))
                    for i in range(no_of_elective):
                        elective = ElectiveSubject.objects.get_or_create(
                            name=request.POST.get('elective_' + str(i + 1)),
                            short_form=request.POST.get(
                                'elective_short_' + str(i + 1)),
                            subject=subject_obj,
                            is_active=True)
                        ElectiveDivision.objects.create(elective_subject=elective)

                    subject_obj.save()
                    BranchSubject.objects.get_or_create(year_branch=year_branch_obj,
                                                        semester=semester_obj,
                                                        subject=subject_obj,
                                                        is_active=True)
                    return render(request, 'test_register_subject.html', {
                        'class_active': class_active,
                        'form': SubjectForm(),
                        'success': 'Subject with electives registered successfully'
                    })

                else:
                    subject_obj = subject_form.save(commit=False)
                    subject_obj.save()
                    BranchSubject.objects.get_or_create(year_branch=year_branch_obj,
                                                        semester=semester_obj,
                                                        subject=subject_obj,
                                                        is_active=True)
                    return render(request, 'test_register_subject.html', {
                        'class_active': class_active,
                        'form': SubjectForm(),
                        'success': 'Subject registered successfully'
                    })

            else:
                print(subject_form.errors)
                return render(request, 'test_register_subject.html', {
                    'class_active': class_active,
                    'form': subject_form,
                    'error': 'Form not valid. fill again with correction'
                })
        elif request.method == 'GET':

            return render(request, 'test_register_subject.html', {
                'class_active': class_active,
                'form': SubjectForm(),
            })

    return HttpResponseRedirect('/')


def change_password(request):
    if request.method == 'POST':
        gr_number = request.POST.get('gr_number')
        new = request.POST.get('new_pwd')
        cnf = request.POST.get('cnf_pwd')
        try:
            user = User.objects.get(username=gr_number)
        except:
            return render(request, 'login.html', {'error': 'No user found.'})
        if new != cnf:
            return render(request, 'change_password.html', {
                'error': "Confirm Password didn't match new Password!",
                'gr_number': gr_number
            })
        else:
            user.set_password(new)
            user.save()
            student = Student.objects.get(user=user)
            student.key = 'verified'
            student.save()
            return render(request, 'login.html', {
                'success': "Password is successfully changed",
            })
    else:
        return render(request, 'change_password.html')


def forgot_password(request):
    if request.method == 'POST':
        gr_number = request.POST.get('gr_number')
        try:
            user = User.objects.get(username=gr_number)
        except User.DoesNotExist:
            return render(request, 'forgot_password.html', {'error': 'No User exist with ' + gr_number})
        try:
            student = Student.objects.get(user=user)
        except:
            return render(request, 'forgot_password.html', {'error': 'Student not found with this email.'})

        if email_sending_service_enabled:

            student.key = generate_activation_key()
            student.save()
            link = conf.site_initial_link + '/register/verification/email/' + student.key + \
                   '/' + user.username
            send_mail('VIIT Forgot Password Link',
                      link,
                      'noreply.viit@gmail.com',
                      [user.email], fail_silently=False)
            return render(request, 'login.html',
                          {'success': 'Mail has been successfully sent to ' + user.email,
                           })
        else:
            return render(request, 'forgot_password.html',
                          {'error': 'Mail service is temporarily out of coverage.'})

    else:
        return render(request, 'forgot_password.html')


def verification_process(request, key, username):
    try:
        user = User.objects.get(username=username)
        student = Student.objects.get(user=user)
    except:
        return render(request, 'login.html', {'error': 'Something is wrong.'})
    if student.key == 'verified':
        return render(request, 'login.html', {'error': 'Something is wrong.'})
    if student:
        if request.method == 'POST':
            if student.key == key:
                gr_number = request.POST.get('gr_number')
                new = request.POST.get('new_pwd')
                cnf = request.POST.get('cnf_pwd')
                try:
                    user = User.objects.get(username=gr_number)
                except:
                    return render(request, 'login.html', {'error': 'No user found.'})
                if new != cnf:
                    return render(request, 'change_password.html', {
                        'error': "Confirm Password didn't match new Password!",
                        'gr_number': gr_number
                    })
                else:
                    user.set_password(new)
                    user.save()
                    student = Student.objects.get(user=user)
                    student.key = 'verified'
                    student.save()
                    return render(request, 'login.html', {
                        'success': "Password is successfully changed",
                    })
        elif request.method == 'GET':
            if student.key == key:
                return render(request, 'change_password.html', {'gr_number': student.gr_number,
                                                                'key': key})
            else:
                return render(request, 'login.html', {'error': 'Something is wrong.'})
    else:
        return render(request, 'login.html', {'error': 'Something is wrong.'})


def set_schedule_date(request):
    class_active = "set_date"
    user = request.user
    if not user.is_anonymous:
        if request.method == 'GET':
            form = DateScheduleForm()
            return render(request, 'set_schedule_date.html', {
                'class_active': class_active,
                'form': form
            })
        else:
            form = DateScheduleForm(request.POST)
            if form.is_valid():
                obj = form.save()
                # below code is only for subject registration of student
                notification_type = 'general'
                message = 'Subject Registration has been Scheduled from ' + obj.start_date.__str__() + ' to ' + obj.end_date.__str__()
                heading = 'Subject Registration'
                type = 'forward'
                user_type = 'Student'
                action = '/register/student_subject/'
                division = Division.objects.filter(is_active=True)
                notify_users(notification_type=notification_type, message=message, type=type, user_type=user_type,
                             action=action, division=division, heading=heading)
                return render(request, 'set_schedule_date.html', {
                    'class_active': class_active,
                    'success': 'Successfully saved',
                    'form': form
                })
            else:
                return render(request, 'set_schedule_date.html', {
                    'class_active': class_active,
                    'form': form
                })

    else:
        return redirect('/login/')


# def student_subject_registration(request):
#     user = request.user
#     if not user.is_anonymous:
#         if has_role(user, 'student'):
#             student = user.student
#             batch = student.batch
#             division = batch.division
#             # year_branch
#             return render(request, 'student_subject_registration.html')


# def load_student_detail():
#     all_students = Student.objects.all()
#     for each_student in all_students:
#         try:
#             curr_roll = gr_roll_dict[each_student.gr_number]
#             branch = Branch.objects.get(branch='Computer')
#             year = CollegeYear.objects.get(year='TE')
#             curr_division = CollegeExtraDetail.objects.get(branch=branch, year=year, division='B', shift__shift=1)
#
#             curr_batch = Batch.objects.get(division=curr_division, batch_name='B1' if int(curr_roll) in range(322001, 322022)
#                                            else 'B2' if int(curr_roll) in range(322022, 322044)
#                                            else 'B3' if int(curr_roll) in range(322044, 322066)
#                                            else 'B4')
#             StudentDetail.objects.create(
#                 student=each_student,
#                 batch=curr_batch,
#                 roll_number=curr_roll
#             )
#             print('Created ', each_student.first_name)
#         except:
#             pass
#
#     return HttpResponse(StudentDetail.objects.all())
#
# load_student_detail()

# i = 1
# while (i < 43):
#     if i != 11 and i!= 12:
#         student_detail = StudentDetail.objects.get(student__gr_number='MECH' + str(i))
#         student_detail.semester = Semester.objects.get(semester=1, is_active=True)
#         student_detail.save()
#         print('MECH' + str(i) + ' Done')
#     student_detail = StudentDetail.objects.get(student__gr_number='ENTC' + str(i))
#     student_detail.semester = Semester.objects.get(semester=1, is_active=True)
#     student_detail.save()
#     print('ENTC' + str(i) + ' Done')
#     i += 1


# def auto_student_subject(request):
#     if request.method == 'POST':
#         user = request.user
#         is_student = RoleManager.objects.filter(user=user, role__role='student')
#         is_faculty = RoleManager.objects.filter(user=user, role__role='faculty')
#         students = StudentDetail.objects.filter(batch__division__year_branch__branch__branch='Computer', is_active=True ).values_list('student', flat=True).distinct()
#         for student in students:
#
#             # if i != 11 and i != 12:
#             if is_student:
#                 student_new_detail = 0
#                 try:
#
#                     student = Student.objects.get(gr_number=str(student))
#                     student_detail = StudentDetail.objects.get(student=student, is_active=True)
#
#                     branch_obj = Branch.objects.get(branch='Computer')
#                     year_obj = CollegeYear.objects.get(year='TE')
#                     year_branch = YearBranch.objects.get(year=year_obj, branch=branch_obj, is_active=True)
#                     division_obj = Division.objects.get(year_branch=year_branch, division='B', is_active=True)
#                     batch_obj = Batch.objects.get(division=division_obj, batch_name='B1')
#                     student_detail.batch = batch_obj
#                     student_detail.semester = Semester.objects.get(semester=1, is_active=True)
#                     student_detail.save()
#
#                     subjects = BranchSubject.objects.filter(year_branch=student_detail.batch.division.year_branch,
#                                                             is_active=True)
#                     no_of_semester = student_detail.batch.division.year_branch.year.no_of_semester
#                     student_curr_sem_obj = student_detail.semester
#                     student_curr_year_obj = student_detail.batch.division.year_branch.year
#                     next_sem = (student_curr_sem_obj.semester % no_of_semester) + 1
#                     try:
#                         next_sem_obj = Semester.objects.get(semester=next_sem, is_active=True)
#                     except:
#                         return render(request, 'register_student_subject.html',
#                                       context={'error': 'Semester object getting error!'})
#                     if student_curr_sem_obj.semester == no_of_semester:
#                         try:
#                             next_year_obj = CollegeYear.objects.get(number=(student_curr_year_obj.number + 1))
#
#                         except Exception as e:
#                             return render(request, 'show_student_subject.html',
#                                           context={'error': 'You are in final year.',
#                                                    'subjects': StudentSubject.objects.filter(student=student,
#                                                                                              is_active=True).values_list(
#                                                        'subject', flat=True)
#                                                    })
#                         try:
#                             student_new_detail = StudentDetail.objects.get_or_create(student=student_detail.student,
#                                                                                      semester=next_sem_obj, is_active=True)[
#                                 0]
#                             next_batch_obj = Batch.objects.get_or_create(batch_name=student_detail.batch.batch_name,
#                                                                          division=Division.objects.get_or_create(
#                                                                              division=student_detail.batch.division.division,
#                                                                              shift=student_detail.batch.division.shift,
#                                                                              year_branch=YearBranch.objects.get(
#                                                                                  year=next_year_obj,
#                                                                                  branch=student_detail.batch.division.year_branch.branch))[
#                                                                              0])[0]
#                             student_new_detail.batch = next_batch_obj
#                             student_new_detail.save()
#
#                         except Exception as e:
#                             print(e)
#                             return render(request, 'register_student_subject.html',
#                                           context={'error': 'Next batch creation failed!'})
#                     else:
#                         student_new_detail = StudentDetail.objects.get_or_create(student=student_detail.student,
#                                                                                  semester=next_sem_obj, is_active=True)[0]
#                         next_batch_obj = Batch.objects.get_or_create(batch_name=student_detail.batch.batch_name,
#                                                                      division=student_detail.batch.division)[0]
#                         student_new_detail.batch = next_batch_obj
#                         student_new_detail.save()
#
#                     # ================Validation elective subs count=======================================
#                     electives_groups = BranchSubject.objects.filter(
#                         year_branch=student_new_detail.batch.division.year_branch,
#                         semester=student_new_detail.semester,
#                         subject__is_elective_group=True,
#                         subject__is_active=True,
#                         is_active=True)
#                     selected_elective_pks = {}
#                     for each_group in electives_groups:
#                         selected_elective_pks[each_group] = request.POST.getlist(
#                             'elective_subject_' + str(each_group.subject.pk))
#                         if len(selected_elective_pks[each_group]) != 1:
#                             if student_new_detail:
#                                 student_new_detail.is_active = False
#                                 student_new_detail.save()
#                             return render(request, 'dashboard_student.html', context={
#                                 'error': 'You have to select exactly 1 subject for Elective Group ' + each_group.subject.name,
#                                 'info': 'Please go to Subject registration again!'})
#
#                     # ======================================================================================
#                     # ========================inactive all prev subjects====================================
#                     for each in StudentSubject.objects.filter(student=student, is_active=True):
#                         each.is_active = False
#                         each.save()
#                     # ================this is for elective=====================
#                     for each_group in electives_groups:
#                         for each_elective_pk in selected_elective_pks[each_group]:
#                             each_elective_obj = ElectiveSubject.objects.get(pk=each_elective_pk)
#                             elective_division_obj = \
#                                 ElectiveDivision.objects.get_or_create(elective_subject=each_elective_obj,
#                                                                        division=1,
#                                                                        is_active=True)[0]
#                             elective_batch_obj = ElectiveBatch.objects.get_or_create(
#                                 division=elective_division_obj,
#                                 batch_name='Batch 1',
#                                 is_active=True
#                             )[0]
#                             student_subject_obj = StudentSubject.objects.get_or_create(student=student,
#                                                                                        subject=each_group.subject,
#                                                                                        is_active=True)[0]
#                             student_subject_obj.elective_division = elective_division_obj
#                             student_subject_obj.elective_batch = elective_batch_obj
#                             student_subject_obj.save()
#                     # =========================================================
#
#                     regular_subjects = BranchSubject.objects.filter(
#                         year_branch=student_new_detail.batch.division.year_branch,
#                         semester=next_sem_obj,
#                         is_active=True)
#                     for each_regular_sub in regular_subjects:
#                         StudentSubject.objects.get_or_create(student=student,
#                                                              subject=each_regular_sub.subject,
#                                                              is_active=True)
#
#                     student_detail.is_active = False
#                     student_detail.save()
#                     for each in StudentSubject.objects.filter(student=student, is_active=True):
#                         sub_to_inactive = BranchSubject.objects.filter(subject=each.subject,
#                                                                        year_branch=student_detail.batch.division.year_branch,
#                                                                        semester=student_detail.semester,
#                                                                        is_active=True)
#                         if sub_to_inactive:
#                             each.is_active = False
#                             each.save()
#                     student_new_detail.has_registered_subject = True
#                     student_new_detail.last_subject_registration_date = datetime.date.today()
#                     student_new_detail.save()
#                     subjects = BranchSubject.objects.filter(subject__pk__in=StudentSubject.objects.filter(student=student,
#                                                                                                           is_active=True).values_list(
#                         'subject__pk', flat=True), is_active=True)
#                     elective_subjects = [ElectiveSubject.objects.filter(pk=i.elective_division.elective_subject.pk)
#                                          for i in StudentSubject.objects.filter(student=student,
#                                                                                 is_active=True,
#                                                                                 subject__is_active=True,
#                                                                                 subject__is_elective_group=True)]
#                     # return render(request, 'show_student_subject.html', context={'subjects': subjects,
#                     #                                                              'success': 'Subjects registered successfully'})
#                     print('DONE SUBJECT COMP')
#                 except Exception as e:
#                     if student_new_detail != 0:
#                         student_new_detail.is_active = False
#                         student_new_detail.save()
#                     return render(request, 'dashboard_student.html', context={
#                         'error': 'You have error: ' + str(e),
#                         'info': 'Please go to Subject registration again!'})
#             if is_faculty:
#                 return HttpResponse('Faculty')
#
#     elif request.method == 'GET':
#         user = request.user
#         is_student = RoleManager.objects.filter(user=user, role__role='student')
#         is_faculty = RoleManager.objects.filter(user=user, role__role='faculty')
#         if is_student:
#
#             student = Student.objects.get(user=user)
#             try:
#                 schedulable = Schedulable.objects.get(name='Student Subject Registration')
#                 schedule_obj = schedulable.schedule_set.filter(is_active=True)
#                 if len(schedule_obj) != 1:
#                     return HttpResponse('Either you have multiple active or none active')
#                 else:
#                     schedule_obj = schedule_obj[0]
#
#             except:
#                 return render(request, 'register_student_subject.html',
#                               context={'info': 'Subject registration is not started yet.'})
#             if schedule_obj.event_active("Student Subject Registration", datetime.date.today()):
#                 student = Student.objects.get(user=user)
#                 student_detail = StudentDetail.objects.get(student=student, is_active=True)
#                 if student_detail.last_subject_registration_date:
#                     if schedule_obj.event_active('Student Subject Registration',
#                                                  student_detail.last_subject_registration_date):
#                         student_subject_all = StudentSubject.objects.filter(student=student,
#                                                                             subject__is_active=True,
#                                                                             is_active=True)
#                         student_subject_regular = student_subject_all.filter(subject__is_elective_group=False)
#                         student_subject_elective = student_subject_all.filter(subject__is_elective_group=True)
#
#                         subjects = [BranchSubject.objects.get(subject=i.subject, is_active=True) for i in
#                                     student_subject_regular]
#                         elective_subjects = [ElectiveSubject.objects.get(pk=i.elective_division.elective_subject.pk)
#                                              for i in student_subject_elective]
#                         return render(request, 'show_student_subject.html',
#                                       context={'subjects': subjects,
#                                                'elective_subjects': elective_subjects,
#                                                'info': 'Already registered. Your current semester subjects are shown.'})
#
#                 no_of_semester = student_detail.batch.division.year_branch.year.no_of_semester
#                 student_curr_sem_obj = student_detail.semester
#                 student_curr_year_obj = student_detail.batch.division.year_branch.year
#                 next_sem = (student_curr_sem_obj.semester % no_of_semester) + 1
#                 try:
#                     next_sem_obj = Semester.objects.get(semester=next_sem, is_active=True)
#                 except:
#                     return render(request, 'register_student_subject.html',
#                                   context={'error': 'Semester object getting error!'})
#
#                 if student_curr_sem_obj.semester == no_of_semester:
#                     try:
#                         next_year_obj = CollegeYear.objects.get(number=(student_curr_year_obj.number + 1))
#
#                     except Exception as e:
#                         return render(request, 'show_student_subject.html',
#                                       context={'error': 'You are in final year.',
#                                                'subjects': [BranchSubject.objects.get(subject=i.subject,
#                                                                                       is_active=True) for i in
#                                                             StudentSubject.objects.filter(student=student,
#                                                                                           is_active=True)]
#                                                })
#
#                     all_subjects = BranchSubject.objects.filter(year_branch__year=next_year_obj,
#                                                                 semester=next_sem_obj,
#                                                                 year_branch__branch=student_detail.batch.division.year_branch.branch,
#                                                                 is_active=True)
#                     subjects = all_subjects.filter(subject__is_elective_group=False)
#                     elective_subjects = ElectiveSubject.objects.filter(subject__branchsubject__in=
#                     all_subjects.filter(
#                         subject__is_elective_group=True),
#                         is_active=True)
#                 else:
#                     all_subjects = BranchSubject.objects.filter(year_branch=student_detail.batch.division.year_branch,
#                                                                 semester=next_sem_obj,
#                                                                 is_active=True)
#                     subjects = all_subjects.filter(subject__is_elective_group=False)
#                     elective_subjects = ElectiveSubject.objects.filter(subject__branchsubject__in=
#                     all_subjects.filter(
#                         subject__is_elective_group=True),
#                         is_active=True)
#                 return render(request, 'register_student_subject.html', context={'subjects': subjects,
#                                                                                  'elective_subjects': elective_subjects})
#             else:
#                 subjects = [BranchSubject.objects.get(subject=i.subject, is_active=True) for i in
#                             StudentSubject.objects.filter(student=student,
#                                                           subject__is_elective_group=False,
#                                                           subject__is_active=True,
#                                                           is_active=True)]
#
#                 return render(request, 'show_student_subject.html',
#                               context={'subjects': subjects,
#                                        'info': 'Subject registration is not started yet. Your current semester subjects are shown.'})
#         if is_faculty:
#             return HttpResponse('Faculty')
#         return render(request, 'register_student_subject.html')


def student_subject(request):
    if request.method == 'POST':
        user = request.user
        is_student = RoleManager.objects.filter(user=user, role__role='student')
        is_faculty = RoleManager.objects.filter(user=user, role__role='faculty')
        if is_student:
            student_new_detail = 0
            try:
                student = Student.objects.get(user=user)
                student_detail = StudentDetail.objects.get(student=student, is_active=True)

                no_of_semester = student_detail.batch.division.year_branch.year.no_of_semester
                student_curr_sem_obj = student_detail.semester
                student_curr_year_obj = student_detail.batch.division.year_branch.year
                next_sem = (student_curr_sem_obj.semester % no_of_semester) + 1
                try:
                    next_sem_obj = Semester.objects.get(semester=next_sem, is_active=True)
                except:
                    return render(request, 'register_student_subject.html',
                                  context={'error': 'Semester object getting error!'})
                if student_curr_sem_obj.semester == no_of_semester:
                    try:
                        next_year_obj = CollegeYear.objects.get(number=(student_curr_year_obj.number + 1))

                    except Exception as e:
                        return render(request, 'show_student_subject.html',
                                      context={'error': 'You are in final year.',
                                               'subjects': StudentSubject.objects.filter(student=student,
                                                                                         is_active=True).values_list(
                                                   'subject', flat=True)
                                               })
                    try:
                        student_new_detail = StudentDetail.objects.get_or_create(student=student_detail.student,
                                                                                 semester=next_sem_obj, is_active=True)[
                            0]
                        next_batch_obj = Batch.objects.get_or_create(batch_name=student_detail.batch.batch_name,
                                                                     division=Division.objects.get_or_create(
                                                                         division=student_detail.batch.division.division,
                                                                         shift=student_detail.batch.division.shift,
                                                                         year_branch=YearBranch.objects.get(
                                                                             year=next_year_obj,
                                                                             branch=student_detail.batch.division.year_branch.branch))[
                                                                         0])[0]
                        student_new_detail.batch = next_batch_obj
                        student_new_detail.save()

                    except Exception as e:
                        print(e)
                        return render(request, 'register_student_subject.html',
                                      context={'error': 'Next batch creation failed!'})
                else:
                    student_new_detail = StudentDetail.objects.get_or_create(student=student_detail.student,
                                                                             semester=next_sem_obj, is_active=True)[0]
                    next_batch_obj = Batch.objects.get_or_create(batch_name=student_detail.batch.batch_name,
                                                                 division=student_detail.batch.division)[0]
                    student_new_detail.batch = next_batch_obj
                    student_new_detail.save()

                # ================Validation elective subs count=======================================
                electives_groups = BranchSubject.objects.filter(
                    year_branch=student_new_detail.batch.division.year_branch,
                    semester=student_new_detail.semester,
                    subject__is_elective_group=True,
                    subject__is_active=True,
                    is_active=True)
                selected_elective_pks = {}
                for each_group in electives_groups:
                    selected_elective_pks[each_group] = request.POST.getlist(
                        'elective_subject_' + str(each_group.subject.pk))
                    if len(selected_elective_pks[each_group]) != 1:
                        if student_new_detail:
                            student_new_detail.is_active = False
                            student_new_detail.save()
                        return render(request, 'dashboard_student.html', context={
                            'error': 'You have to select exactly 1 subject for Elective Group ' + each_group.subject.name,
                            'info': 'Please go to Subject registration again!'})

                # ======================================================================================
                # ========================inactive all prev subjects====================================
                for each in StudentSubject.objects.filter(student=student, is_active=True):
                    each.is_active = False
                    each.save()
                # ================this is for elective=====================
                for each_group in electives_groups:
                    for each_elective_pk in selected_elective_pks[each_group]:
                        each_elective_obj = ElectiveSubject.objects.get(pk=each_elective_pk)
                        elective_division_obj = \
                            ElectiveDivision.objects.get_or_create(elective_subject=each_elective_obj,
                                                                   division=1,
                                                                   is_active=True)[0]
                        elective_batch_obj = ElectiveBatch.objects.get_or_create(
                            division=elective_division_obj,
                            batch_name='Batch 1',
                            is_active=True
                        )[0]
                        student_subject_obj = StudentSubject.objects.get_or_create(student=student,
                                                                                   subject=each_group.subject,
                                                                                   is_active=True)[0]
                        student_subject_obj.elective_division = elective_division_obj
                        student_subject_obj.elective_batch = elective_batch_obj
                        student_subject_obj.save()
                # =========================================================

                regular_subjects = BranchSubject.objects.filter(
                    year_branch=student_new_detail.batch.division.year_branch,
                    semester=next_sem_obj,
                    is_active=True)
                for each_regular_sub in regular_subjects:
                    StudentSubject.objects.get_or_create(student=student,
                                                         subject=each_regular_sub.subject,
                                                         is_active=True)

                student_detail.is_active = False
                student_detail.save()
                for each in StudentSubject.objects.filter(student=student, is_active=True):
                    sub_to_inactive = BranchSubject.objects.filter(subject=each.subject,
                                                                   year_branch=student_detail.batch.division.year_branch,
                                                                   semester=student_detail.semester,
                                                                   is_active=True)
                    if sub_to_inactive:
                        each.is_active = False
                        each.save()
                student_new_detail.has_registered_subject = True
                student_new_detail.last_subject_registration_date = datetime.date.today()
                student_new_detail.save()
                subjects = BranchSubject.objects.filter(subject__pk__in=StudentSubject.objects.filter(student=student,
                                                                                                      is_active=True).values_list(
                    'subject__pk', flat=True), is_active=True)
                elective_subjects = [ElectiveSubject.objects.filter(pk=i.elective_division.elective_subject.pk)
                                     for i in StudentSubject.objects.filter(student=student,
                                                                            is_active=True,
                                                                            subject__is_active=True,
                                                                            subject__is_elective_group=True)]
                return render(request, 'show_student_subject.html', context={'subjects': subjects,
                                                                             'success': 'Subjects registered successfully'})
            except Exception as e:
                if student_new_detail != 0:
                    student_new_detail.is_active = False
                    student_new_detail.save()
                return render(request, 'dashboard_student.html', context={
                    'error': 'You have error: ' + str(e),
                    'info': 'Please go to Subject registration again!'})
        if is_faculty:
            return HttpResponse('Faculty')
    elif request.method == 'GET':
        user = request.user
        is_student = RoleManager.objects.filter(user=user, role__role='student')
        is_faculty = RoleManager.objects.filter(user=user, role__role='faculty')
        if is_student:

            student = Student.objects.get(user=user)
            try:
                schedulable = Schedulable.objects.get(name='Student Subject Registration')
                schedule_obj = schedulable.schedule_set.filter(is_active=True)
                if len(schedule_obj) != 1:
                    return HttpResponse('Either you have multiple active or none active')
                else:
                    schedule_obj = schedule_obj[0]

            except:
                return render(request, 'register_student_subject.html',
                              context={'info': 'Subject registration is not started yet.'})
            if schedule_obj.event_active("Student Subject Registration", datetime.date.today()):
                student = Student.objects.get(user=user)
                student_detail = StudentDetail.objects.get(student=student, is_active=True)
                if student_detail.last_subject_registration_date:
                    if schedule_obj.event_active('Student Subject Registration',
                                                 student_detail.last_subject_registration_date):
                        student_subject_all = StudentSubject.objects.filter(student=student,
                                                                            subject__is_active=True,
                                                                            is_active=True)
                        student_subject_regular = student_subject_all.filter(subject__is_elective_group=False)
                        student_subject_elective = student_subject_all.filter(subject__is_elective_group=True)

                        subjects = [BranchSubject.objects.get(subject=i.subject, is_active=True) for i in
                                    student_subject_regular]
                        elective_subjects = [ElectiveSubject.objects.get(pk=i.elective_division.elective_subject.pk)
                                             for i in student_subject_elective]
                        return render(request, 'show_student_subject.html',
                                      context={'subjects': subjects,
                                               'elective_subjects': elective_subjects,
                                               'info': 'Already registered. Your current semester subjects are shown.'})

                no_of_semester = student_detail.batch.division.year_branch.year.no_of_semester
                student_curr_sem_obj = student_detail.semester
                student_curr_year_obj = student_detail.batch.division.year_branch.year
                next_sem = (student_curr_sem_obj.semester % no_of_semester) + 1
                try:
                    next_sem_obj = Semester.objects.get(semester=next_sem, is_active=True)
                except:
                    return render(request, 'register_student_subject.html',
                                  context={'error': 'Semester object getting error!'})

                if student_curr_sem_obj.semester == no_of_semester:
                    try:
                        next_year_obj = CollegeYear.objects.get(number=(student_curr_year_obj.number + 1))

                    except Exception as e:
                        return render(request, 'show_student_subject.html',
                                      context={'error': 'You are in final year.',
                                               'subjects': [BranchSubject.objects.get(subject=i.subject,
                                                                                      is_active=True) for i in
                                                            StudentSubject.objects.filter(student=student,
                                                                                          is_active=True)]
                                               })

                    all_subjects = BranchSubject.objects.filter(year_branch__year=next_year_obj,
                                                                semester=next_sem_obj,
                                                                year_branch__branch=student_detail.batch.division.year_branch.branch,
                                                                is_active=True)
                    subjects = all_subjects.filter(subject__is_elective_group=False)
                    elective_subjects = ElectiveSubject.objects.filter(subject__branchsubject__in=
                    all_subjects.filter(
                        subject__is_elective_group=True),
                        is_active=True)
                else:
                    all_subjects = BranchSubject.objects.filter(year_branch=student_detail.batch.division.year_branch,
                                                                semester=next_sem_obj,
                                                                is_active=True)
                    subjects = all_subjects.filter(subject__is_elective_group=False)
                    elective_subjects = ElectiveSubject.objects.filter(subject__branchsubject__in=
                    all_subjects.filter(
                        subject__is_elective_group=True),
                        is_active=True)
                return render(request, 'register_student_subject.html', context={'subjects': subjects,
                                                                                 'elective_subjects': elective_subjects})
            else:
                subjects = [BranchSubject.objects.get(subject=i.subject, is_active=True) for i in
                            StudentSubject.objects.filter(student=student,
                                                          subject__is_elective_group=False,
                                                          subject__is_active=True,
                                                          is_active=True)]

                return render(request, 'show_student_subject.html',
                              context={'subjects': subjects,
                                       'info': 'Subject registration is not started yet. Your current semester subjects are shown.'})
        if is_faculty:
            return HttpResponse('Faculty')
        return render(request, 'register_student_subject.html')


def register_year(request):
    class_active = 'register'
    user = request.user
    if not user.is_anonymous:
        branches = Branch.objects.all()
        if request.method == 'GET':
            return render(request, 'register_year.html', {
                'class_active': class_active,
                'branches': branches,
            })
        elif request.method == 'POST':
            year = request.POST.get('year')
            branch = request.POST.get('branch')

            no_of_sem = request.POST.get('no_of_sem')
            # for i in range(int(no_of_sem)):
            #     Semester.objects.create(semester=i+1)
            year_number = request.POST.get('year_number')

            year_obj = CollegeYear.objects.get_or_create(year=year, no_of_semester=no_of_sem, number=year_number)
            branch_obj = Branch.objects.get(branch=branch)
            for i in range(int(no_of_sem)):
                try:
                    sem_obj = Semester.objects.get(semester=i + 1, is_active=True)
                    # print(i+1, 'try')
                except:
                    sem_obj = Semester.objects.create(semester=i + 1)
                    # print(i+1, 'except')
                year_branch_obj = YearBranch.objects.get_or_create(year=year_obj[0], branch=branch_obj, is_active=True)
                YearSemester.objects.get_or_create(semester=sem_obj, year_branch=year_branch_obj[0])
                Shift.objects.get_or_create(year_branch=year_branch_obj[0], shift=request.POST.get('no_of_shift'))

            return render(request, 'register_year.html', {
                'class_active': class_active,
                'branches': branches,
                'success': 'Year ' + year + ' Saved!'
            })
        return HttpResponse('Something is wrong!')
    return HttpResponseRedirect('/login/')


def register_year_detail(request):
    class_active = "register"
    user = request.user
    if not user.is_anonymous:
        branches = Branch.objects.all()
        years = CollegeYear.objects.all()
        year_semester_json = {}
        for obj in YearSemester.objects.all():
            branch = obj.year_branch.branch.branch
            year = obj.year_branch.year.year
            semester = obj.semester.semester
            if branch in year_semester_json:
                if year in year_semester_json[branch]:
                    {}
                else:
                    year_semester_json[branch][year] = []
            else:
                year_semester_json[branch] = {}
                year_semester_json[branch][year] = []
            year_semester_json[branch][year] += [semester]

        if request.method == 'GET':
            return render(request, 'register_year_details.html', {
                'class_active': class_active,
                'branches': branches,
                'years': years,
                'year_semester': year_semester_json
            })

        elif request.method == 'POST':
            branch = request.POST.get('branch')
            year = request.POST.get('year')
            semester = request.POST.get('semester')
            # no_of_semester = request.POST.get('no_of_semester')
            branch_obj = Branch.objects.get(branch=branch)
            year_obj = CollegeYear.objects.get(year=year)
            semester_obj = Semester.objects.get(semester=semester)
            year_branch_obj = YearBranch.objects.get(branch=branch_obj, year=year_obj, is_active=True)
            # number_of_elective_groups = int(request.POST.get('elective_number'))
            semester_start_date = parse_date(request.POST.get('semester_start_date'))
            semester_end_date = parse_date(request.POST.get('semester_end_date'))

            if semester_end_date < semester_start_date:
                return render(request, 'register_year_details.html', {
                    'class_active': class_active,
                    'branches': branches,
                    'years': years,
                    'year_semester': year_semester_json,
                    'error': 'Semester end date cannot be less than semester start date'
                })

            lecture_start_date = parse_date(request.POST.get('lecture_start_date'))
            lecture_end_date = parse_date(request.POST.get('lecture_end_date'))

            if lecture_end_date < lecture_start_date:
                return render(request, 'register_year_details.html', {
                    'class_active': class_active,
                    'branches': branches,
                    'years': years,
                    'year_semester': year_semester_json,
                    'error': 'lecture end date cannot be less than lecture start date'
                })

            # for i in range(number_of_elective_groups):
            #     ElectiveGroup.objects.create(year_branch=year_branch_obj, semester=semester_obj,
            #                                  group=chr(i + 65))
            year_branch_obj = YearBranch.objects.get(year=year_obj, branch=branch_obj, is_active=True)
            year_sem_obj = YearSemester.objects.get(year_branch=year_branch_obj, semester=semester_obj, is_active=True)
            year_sem_obj.start_date = semester_start_date
            year_sem_obj.end_date = semester_end_date
            year_sem_obj.lecture_start_date = lecture_start_date
            year_sem_obj.lecture_end_date = lecture_end_date
            # year_sem_obj.number_of_electives_groups = number_of_elective_groups
            year_sem_obj.save()

            return render(request, 'register_year_details.html', {
                'class_active': class_active,
                'branches': branches,
                'years': years,
                'year_semester': year_semester_json,
                'success': 'Successfully registered details'
            })
    return HttpResponseRedirect('/login/')


def student_subject_division(request):
    class_active = 'register'
    if request.method == 'GET':

        return render(request, 'student_subject_division.html', {
            'class_active': class_active,
            'form': YearBranchSemForm,
            'select_year_branch_sem': True})

    elif request.method == 'POST' and request.POST.get('select_year_branch_sem_button'):
        year_branch_sem_form = YearBranchSemForm(request.POST)
        if year_branch_sem_form.is_valid():
            year_obj = CollegeYear.objects.get(pk=year_branch_sem_form.cleaned_data.get('year'))
            branch_obj = Branch.objects.get(pk=year_branch_sem_form.cleaned_data.get('branch'))
            semester_obj = Semester.objects.get(pk=year_branch_sem_form.cleaned_data.get('semester'))
            year_branch = YearBranch.objects.get(year=year_obj,
                                                 branch=branch_obj,
                                                 is_active=True)
            subjects_all = BranchSubject.objects.filter(year_branch=year_branch,
                                                        semester=semester_obj,
                                                        is_active=True)
            subjects_regular = subjects_all.filter(subject__is_elective_group=False)
            subjects_elective_group = subjects_all.filter(subject__is_elective_group=True)
            elective_subjects = ElectiveSubject.objects.filter(subject__branchsubject__in=subjects_elective_group,
                                                               is_active=True)
            return render(request, 'student_subject_division.html', {
                'class_active': class_active,
                'selected_year': year_obj.year,
                'selected_branch': branch_obj.branch,
                'selected_semester': semester_obj.semester,
                'select_subjects': True,
                'regular_subjects': subjects_regular,
                'elective_subjects': elective_subjects})

    elif request.POST.get('selected_subject_link'):
        selected_subject = request.POST.get('selected_subject_link')
        selected_subject_obj = BranchSubject.objects.get(pk=selected_subject)
        student_subjects = StudentSubject.objects.filter(subject=selected_subject_obj.subject,
                                                         is_active=True)
        year_branch_obj = selected_subject_obj.year_branch
        return render(request, 'student_subject_division.html', {
            'class_active': class_active,
            'selected_year': year_branch_obj.year.year,
            'selected_branch': year_branch_obj.branch.branch,
            'selected_semester': selected_subject_obj.semester.semester,
            'selected_subject_obj': selected_subject_obj,
            'select_student_division': True,
            'student_subjects': student_subjects, })
    elif request.POST.get('selected_subject_elective_link'):
        selected_elective = request.POST.get('selected_subject_elective_link')
        selected_elective_subject_obj = ElectiveSubject.objects.get(pk=selected_elective)
        student_subjects = StudentSubject.objects.filter(subject=selected_elective_subject_obj.subject,
                                                         elective_division__elective_subject=selected_elective_subject_obj,
                                                         elective_division__is_active=True,
                                                         is_active=True)
        selected_semester = request.POST.get('selected_semester')
        selected_branch = request.POST.get('selected_branch')
        selected_year = request.POST.get('selected_year')

        elective_divisions = list(ElectiveDivision.objects.filter(
            elective_subject=selected_elective_subject_obj,
            is_active=True))
        division_batch = {}
        for each_division in elective_divisions:
            # a=list(each_division.electivebatch_set.all())
            division_batch[each_division.pk] = list(
                each_division.electivebatch_set.all().values_list('batch_name', flat=True))
        return render(request, 'student_subject_division.html', {
            'class_active': class_active,
            'selected_semester': selected_semester,
            'selected_branch': selected_branch,
            'selected_year': selected_year,
            'selected_subject_obj': selected_elective_subject_obj,
            'select_student_division': True,
            'selected_sub_name': selected_elective_subject_obj.name,
            'student_subjects': student_subjects,
            'divisions': elective_divisions,
            'division_batch': json.dumps(division_batch)})

    elif request.POST.get('select_division_student_button'):
        selected_division_student_pks = request.POST.getlist('selected_division_student')
        selected_elective_subject_obj = ElectiveSubject.objects.get(pk=request.POST.get('selected_subject'))
        for each in selected_division_student_pks:
            each_division_pk = each.split('_student_')[0]
            each_student_pk = each.split('_student_')[1]
            selected_division_obj = ElectiveDivision.objects.get(pk=each_division_pk)
            for_student = Student.objects.get(pk=each_student_pk)

            selected_elective_batch_obj = ElectiveBatch.objects.get(
                batch_name=request.POST.get('selected_division_student_batch_' + each_student_pk),
                division=selected_division_obj,
                is_active=True)

            student_subject_obj = StudentSubject.objects.get_or_create(student=for_student,
                                                                       subject=selected_elective_subject_obj.subject,
                                                                       is_active=True)[0]
            student_subject_obj.elective_division = selected_division_obj
            student_subject_obj.elective_batch = selected_elective_batch_obj
            student_subject_obj.save()

        student_subjects = StudentSubject.objects.filter(subject=selected_elective_subject_obj.subject,
                                                         is_active=True)
        selected_semester = request.POST.get('selected_semester')
        selected_branch = request.POST.get('selected_branch')
        selected_year = request.POST.get('selected_year')
        elective_divisions = list(ElectiveDivision.objects.filter(
            elective_subject=selected_elective_subject_obj,
            is_active=True))
        division_batch = {}
        for each_division in elective_divisions:
            # a=list(each_division.electivebatch_set.all())
            division_batch[each_division.division] = list(
                each_division.electivebatch_set.all().values_list('batch_name', flat=True))
        return render(request, 'student_subject_division.html', {
            'class_active': class_active,
            'selected_year': selected_year,
            'selected_branch': selected_branch,
            'selected_semester': selected_semester,
            'selected_subject_obj': selected_elective_subject_obj,
            'select_student_division': True,
            'student_subjects': student_subjects,
            'divisions': elective_divisions,
            'division_batch': json.dumps(division_batch),
            'success': 'elective divisions are assigned successfully.'})


def register_branch(request):
    user = request.user
    if not user.is_anonymous:
        if has_role(user, 'faculty'):
            if request.method == "GET":
                return render(request, 'register_branch.html')

            elif request.method == "POST":
                branch = request.POST.get('branch')
                branch = branch.title()
                if len(Branch.objects.filter(branch=branch)) > 0:
                    return render(request, 'register_branch.html', {
                        'error': branch + ' is already registered.'
                    })
                Branch.objects.create(branch=branch)
                return render(request, 'register_branch.html', {
                    'success': 'Successfully registered ' + branch + ' branch',
                })

        return redirect('/login/')
    return redirect('/login/')


def register_division(request):
    user = request.user
    if not user.is_anonymous:
        if has_role(user, 'faculty'):
            data = {}
            year_branch = YearBranch.objects.filter(is_active=True)
            for each in year_branch:
                if each.branch.branch not in data:
                    data[each.branch.branch] = {}

                data[each.branch.branch][each.year.year] = each.shift_set.count()

            if request.method == "GET":
                return render(request, 'register_division.html', {
                    'data': data,
                })
            else:
                print(request.POST)
                branch = Branch.objects.get(branch=request.POST.get('branch'))
                year = CollegeYear.objects.get(year=request.POST.get('year'))
                year_branch_obj = YearBranch.objects.get(branch=branch, year=year)
                divisions = request.POST.getlist('division')
                shifts = request.POST.getlist('shift')

                for index, value in enumerate(divisions):
                    Division.objects.get_or_create(year_branch=year_branch_obj, division=value,
                                                   shift=Shift.objects.get(year_branch=year_branch_obj,
                                                                           shift=shifts[index]))

            return render(request, 'register_division.html', {
                'success': divisions + 'registered',
                'data': data,
            })

        return redirect('/login/')
    return redirect('/login/')


def register_room(request):
    class_active = "register"
    user = request.user
    if not user.is_anonymous:
        if request.method == "GET":
            return render(request, 'register_room.html',{
                'branches': Branch.objects.all()
            })
        elif request.method == "POST":
            branch = Branch.objects.get(branch=request.POST.get('branch'))
            room = request.POST.get('room_number')
            if request.POST.get('lab'):
                lab = True
            else:
                lab=False

            if len(Room.objects.filter(branch=branch, room_number=room, lab=lab)) > 0:
                return render(request, 'register_room.html', {
                    'error': 'Room already registered'
                })
            else:
                Room.objects.create(branch=branch, room_number=room, lab=lab)
                return render(request, 'register_room.html',{
                    'success': 'Room registered!'
                })

    return redirect('/login/')