# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.utils.dateparse import parse_date

from EnterpriseResourcePlanning import conf
from EnterpriseResourcePlanning.conf import email_sending_service_enabled
from General.models import Division, Shift, StudentDetail, CollegeYear, BranchSubject, Semester, \
    FacultySubject, Batch, YearBranch, ElectiveGroup, StudentSubject, YearSemester
from General.views import notify_users
from Login.views import generate_activation_key
from Registration.models import Student, Branch, Faculty, Subject
from UserModel.models import User, RoleManager, RoleMaster
from .forms import StudentForm, FacultyForm, SubjectForm, FacultySubjectForm, gr_roll_dict, DateScheduleForm
from Configuration.stateConf import states


def has_role(user, role):
    if RoleManager.objects.filter(user=user, role=role, is_active=True).exists():
        return True
    else:
        return False


def view_subjects(request):
    subjects = BranchSubject.objects.filter(year_branch__branch=Branch.objects.get(branch='Computer'))
    return render(request, 'view_subjects.html', {'subjects': subjects})


def register_faculty_subject(request):
    if request.method == 'POST':
        form = FacultySubjectForm(request.POST)
        if form.is_valid():
            faculty = Faculty.objects.get(pk=form.cleaned_data.get('faculty'))
            subject = Subject.objects.get(pk=form.cleaned_data.get('subject'))
            division = Division.objects.get(pk=form.cleaned_data.get('division'))

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

            student.user = new_user

            student.save()

            roll_number = gr_roll_dict[student.gr_number]
            branch_obj = Branch.objects.get(branch=branch)
            year_obj = CollegeYear.objects.get(year=year)
            division_obj = Division.objects.get(year_branch__branch=branch_obj, year_branch__year=year_obj,
                                                division=division, shift__shift=shift)
            batch_obj = Batch.objects.get(division=division_obj, batch_name=batch)
            StudentDetail.objects.create(student=student, batch=batch_obj, roll_number=roll_number)

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
    if not user.is_anonymous:
        if request.method == 'POST':

            subject_form = SubjectForm(request.POST)

            if subject_form.is_valid():
                subject_obj = subject_form.save()
                branch_object = Branch.objects.get(branch=subject_form.cleaned_data.get('branch'))
                year_obj = CollegeYear.objects.get(year=subject_form.cleaned_data.get('year'))
                semester_obj = Semester.objects.get(semester=subject_form.cleaned_data.get('semester'))
                # subject_obj = Subject.objects.get(code=subject_form.cleaned_data.get('code'))
                year_branch_obj = YearBranch.objects.get(branch=branch_object, year=year_obj)
                branch_subject = BranchSubject(year_branch=year_branch_obj,
                                               semester=semester_obj, subject=subject_obj)
                branch_subject.save()

                return render(request, 'test_register_subject.html',
                              {'success': subject_obj.short_form + ' is Successfully registered',
                               'form': SubjectForm()})

            else:
                return HttpResponse('error : ' + str(subject_form.errors))

        elif request.method == 'GET':
            subject_form = SubjectForm()
            all_elective = ElectiveGroup.objects.all()
            elective_json = {}
            for each_elective in all_elective:
                branch = each_elective.year_branch.branch
                year = each_elective.year_branch.year
                semester = each_elective.semester
                if branch in elective_json:
                    if year in elective_json[branch]:
                        if semester in elective_json[branch][year]:
                            {}
                        else:
                            elective_json[branch][year][semester] = {}
                    else:
                        elective_json[branch][year] = {}
                        elective_json[branch][year][semester] = {}
                else:
                    elective_json[branch] = {}
                    elective_json[branch][year] = {}
                    elective_json[branch][year][semester] = {}

        return render(request, 'test_register_subject.html',
                      {'form': subject_form})
    return HttpResponseRedirect('/login')


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
    user = request.user
    if not user.is_anonymous:
        if request.method == 'GET':
            form = DateScheduleForm()
            return render(request, 'set_schedule_date.html', {
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
                action = 'register/student_subject/'
                division = Division.objects.filter(is_active=True)
                notify_users(notification_type=notification_type, message=message, type=type, user_type=user_type,
                             action=action, division=division, heading=heading)
                return render(request, 'set_schedule_date.html', {
                    'success': 'Successfully saved',
                    'form': form
                })
            else:
                return render(request, 'set_schedule_date.html', {
                    'form': form
                })


def student_subject_registration(request):
    user = request.user
    if not user.is_anonymous:
        if has_role(user, 'student'):
            student = user.student
            batch = student.batch
            division = batch.division
            # year_branch
            return render(request, 'student_subject_registration.html')


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


def student_subject(request):
    if request.method == 'POST':
        # if request.POST.get('confirm_student_subject'):
        pass
    elif request.method == 'GET':
        user = request.user
        is_student = RoleManager.objects.filter(user=user, role__role='student')
        is_faculty = RoleManager.objects.filter(user=user, role__role='faculty')
        if is_student:
            student = Student.objects.get(user=user)
            student_detail = StudentDetail.objects.get(student=student)
            subjects = BranchSubject.objects.filter(year_branch=student_detail.batch.division.year_branch)
            # subjects = StudentSubject.objects.filter(student=student)
            return render(request, 'register_student_subject.html', context={'subjects': subjects})
        if is_faculty:
            return HttpResponse('Faculty')
        return render(request, 'register_student_subject.html')


def register_year(request):
    user = request.user
    if not user.is_anonymous:
        if request.method == 'GET':
            return render(request, 'register_year.html')
        elif request.method == 'POST':
            year = request.POST.get('year')

            no_of_sem = request.POST.get('no_of_sem')
            # for i in range(int(no_of_sem)):
            #     Semester.objects.create(semester=i+1)
            year_number = request.POST.get('year_number')
            year_obj = CollegeYear.objects.create(year=year, no_of_sem=no_of_sem, number=year_number)
            for i in range(int(no_of_sem)):
                try:
                    sem_obj = Semester.objects.get(semester=i + 1, is_active=True)
                    # print(i+1, 'try')
                except:
                    sem_obj = Semester.objects.create(semester=i + 1)
                    # print(i+1, 'except')

                YearSemester.objects.create(semester=sem_obj, year=year_obj)
            return render(request, 'register_year.html', context={'success': 'Year ' + year + ' Saved!'})
        return HttpResponse('Something is wrong!')
    return HttpResponseRedirect('/login')


def register_year_detail(request):
    user = request.user
    if not user.is_anonymous:
        branches = Branch.objects.all()
        years = CollegeYear.objects.all()
        year_semester_json = {}
        for yr in years:
            year_semester_json[yr.year] = []
        for yr in years:
            year_semester_obj = YearSemester.objects.filter(year=yr, is_active=True)
            for sem in year_semester_obj:
                year_semester_json[yr.year] += [sem.semester.semester]

        if request.method == 'GET':
            return render(request, 'register_year_details.html', {
                'branches': branches,
                'years': years,
                'year_semester': year_semester_json
            })

        else:
            branch = request.POST.get('branch')
            year = request.POST.get('year')
            semester = request.POST.get('semester')
            # no_of_semester = request.POST.get('no_of_semester')
            branch_obj = Branch.objects.get(branch=branch)
            year_obj = CollegeYear.objects.get(year=year)
            semester_obj = Semester.objects.get(semester=semester)
            year_branch_obj = YearBranch.objects.get(branch=branch_obj, year=year_obj, is_active=True)

            semester_start_date = parse_date(request.POST.get('semester_start_date'))
            semester_end_date = parse_date(request.POST.get('semester_end_date'))

            if semester_end_date < semester_start_date:
                return render(request, 'register_year_details.html', {
                    'branches': branches,
                    'years': years,
                    'year_semester': year_semester_json,
                    'error': 'Semester end date cannot be less than semester start date'
                })

            lecture_start_date = parse_date(request.POST.get('lecture_start_date'))
            lecture_end_date = parse_date(request.POST.get('lecture_end_date'))

            if lecture_end_date < lecture_start_date:
                return render(request, 'register_year_details.html', {
                    'branches': branches,
                    'years': years,
                    'year_semester': year_semester_json,
                    'error': 'lecture end date cannot be less than lecture start date'
                })

            ElectiveGroup.objects.create(year_branch=year_branch_obj, semester=semester_obj,
                                         number_of_electives=int(request.POST.get('elective_number')))
            YearSemester.objects.create(year=year_obj, semester=semester_obj, start_date=semester_start_date,
                                        end_date=semester_end_date, lecture_start_date=lecture_start_date,
                                        lecture_end_date=lecture_end_date)

            return render(request, 'register_year_details.html', {
                'branches': branches,
                'years': years,
                'year_semester': year_semester_json,
                'success': 'Successfully registered details'
            })
    return HttpResponseRedirect('/login')
