import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
import datetime

# Create your views here.
from Exam.forms import ExamDetailForm
from Exam.models import ExamMaster, ExamSubject, ExamDetail
from General.models import Semester, BranchSubject, CollegeYear, YearBranch, FacultySubject, Division, StudentDetail
from General.views import notify_users
from Registration.models import Branch
from Registration.views import has_role


def exam_register(request):
    if request.method == 'GET':
        return render(request, 'exam_register.html')

    else:
        exam_name = request.POST.get('exam_name')
        ExamMaster.objects.create(exam_name=exam_name, start_date=datetime.date.today())
        context = {'success': "Successfully registered"}
        return render(request, 'exam_register.html', context)


def exam_detail(request):
    if request.method == "GET":
        return render(request, 'exam_detail.html', {'form': ExamDetailForm})
    else:
        form = ExamDetailForm(request.POST)
        if form.is_valid():
            exam_detail_obj = form.save()
            subjects = request.POST.getlist('subject')
            # Notify students about exam
            notification_type = 'general'
            message = 'Your ' + exam_detail_obj.exam.exam_name + ' exam has been scheduled from ' + \
                      exam_detail_obj.schedule_start_date.__str__() + ' to ' + exam_detail_obj.schedule_end_date.__str__() + \
                      ' for subjects ' + ", ".join(subjects)
            heading = 'Exam Schedule for ' + exam_detail_obj.exam.exam_name

            year_branch_obj = exam_detail_obj.year
            division = list(Division.objects.filter(is_active=True, year_branch=year_branch_obj))

            notify_users(notification_type=notification_type, message=message, heading=heading, division=division)

            user_obj = []
            for each_subject in subjects:
                subject = BranchSubject.objects.get(is_active=True, year_branch=exam_detail_obj.year,
                                                    subject__short_form=each_subject).subject
                faculty_initials = request.POST.get(each_subject + '_faculty')

                faculty_obj = FacultySubject.objects.filter(faculty__initials=faculty_initials, is_active=True,
                                                            subject=subject)[0].faculty

                ExamSubject.objects.create(exam=exam_detail_obj, subject=subject, coordinator=faculty_obj)
                # user_obj.append(faculty_obj.user)
                # Notify Faculty about exam
                notification_type = 'specific'
                message = 'You have been selected as Exam coordinator for ' + exam_detail_obj.exam.exam_name + ' exam which is scheduled from ' + \
                          exam_detail_obj.schedule_start_date.__str__() + ' to ' + exam_detail_obj.schedule_end_date.__str__() + \
                          ' for subject ' + subject.short_form
                heading = 'Exam Schedule for ' + exam_detail_obj.exam.exam_name

                # year_branch_obj = exam_detail_obj.year
                # division = list(Division.objects.filter(is_active=True, year_branch=year_branch_obj))
                notify_users(notification_type=notification_type, message=message, heading=heading,
                             users_obj=[faculty_obj.user],
                             user_type='faculty')
            return redirect('/exam/detail/')
        else:
            return render(request, 'exam_detail.html', {
                'form': form,
                'error': 'Not valid'
            })


def get_subjects(request):
    if request.is_ajax():
        if request.method == "POST":
            year = request.POST.get('year')
            semester = request.POST.get('semester')
            semester_obj = Semester.objects.get(pk=semester)
            # year_splitted = year.split(' ')
            # branch = year_splitted[0]
            # year = year_splitted[1]
            # branch_obj = Branch.objects.get(branch=branch)
            # year_obj = CollegeYear.objects.get(year=year)
            year_branch_obj = YearBranch.objects.get(pk=year)

            subjects = BranchSubject.objects.filter(year_branch=year_branch_obj, semester=semester_obj, is_active=True)

            subject_faculty_json = {}

            for each_subject in subjects:
                short_form = each_subject.subject.short_form
                facultys = set(FacultySubject.objects.filter(subject=each_subject.subject, is_active=True).values_list(
                    'faculty__initials', flat=True))
                subject_faculty_json[short_form] = list(facultys)

            return HttpResponse(json.dumps(subject_faculty_json))

        else:
            return HttpResponse("Not post")
    else:
        return HttpResponse('Not ajax')


def view_exam(request):
    user = request.user
    if has_role(user, 'Student'):
        student_obj = user.student
        student_detail_obj = StudentDetail.objects.get(student=student_obj, is_active=True)
        year_branch_obj = student_detail_obj.batch.division.year_branch
        ExamDetail.objects.filter(is_active=True, year=year_branch_obj)
        return render(request,'view_exam.html')