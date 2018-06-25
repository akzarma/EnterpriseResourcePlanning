import json

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
import datetime
import dateutil.parser

# Create your views here.
from Exam.forms import ExamDetailForm
from Exam.models import ExamMaster, ExamSubject, ExamDetail, ExamGroupDetail
from General.models import Semester, BranchSubject, CollegeYear, YearBranch, FacultySubject, Division, StudentDetail
from General.views import notify_users
from Registration.models import Branch
from Registration.views import has_role
from Timetable.models import Room


def exam_register(request):
    class_active = "exam"
    if request.method == 'GET':
        return render(request, 'exam_register.html', {
            'class_active': class_active,

        })

    else:
        exam_name = request.POST.get('exam_name')
        ExamMaster.objects.create(exam_name=exam_name, start_date=datetime.date.today())
        context = {'success': "Successfully registered"}
        return render(request, 'exam_register.html', context)


def exam_detail(request):
    class_active = 'exam'
    if request.method == "GET":
        return render(request, 'exam_detail.html', {
            'class_active': class_active,
            'form': ExamDetailForm
        })
    else:
        form = ExamDetailForm(request.POST)
        if form.is_valid():
            exam_detail_obj = form.save()
            subjects = request.POST.getlist('subject')

            for each_subject in subjects:
                subject = BranchSubject.objects.get(is_active=True, year_branch=exam_detail_obj.year,
                                                    subject__short_form=each_subject).subject
                faculty_initials = request.POST.get(each_subject + '_faculty')

                faculty_obj = FacultySubject.objects.filter(faculty__initials=faculty_initials, is_active=True,
                                                            subject=subject)[0].faculty

                ExamSubject.objects.create(exam=exam_detail_obj, subject=subject, coordinator=faculty_obj,is_active=True)

            return render(request, 'set_exam_time.html', {
                'subjects': subjects,
                'exam_name': exam_detail_obj.exam.exam_name,
                'branch': exam_detail_obj.year.branch.branch,
                'exam_pk': exam_detail_obj.id,
            })
        else:
            return render(request, 'exam_detail.html', {
                'class_active': class_active,
                'form': form,
                'error': 'Not valid'
            })


def set_exam_time(request):
    user = request.user

    if has_role(user, 'faculty'):
        if request.method == 'POST':
            exam_pk = request.POST.get('exam_pk')
            exam_detail_obj = ExamDetail.objects.get(id=exam_pk)

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

            # Add to examsubject
            user_obj = []
            for each_exam_subject in exam_detail_obj.examsubject_set.all():

                each_subject = each_exam_subject.subject.short_form

                exam_start_time = dateutil.parser.parse(request.POST.get('start_' + each_subject))
                exam_end_time = dateutil.parser.parse(request.POST.get('end_' + each_subject))

                each_exam_subject.start_datetime = exam_start_time
                each_exam_subject.end_datetime = exam_end_time
                # each_exam_subject.start_datetime

                # user_obj.append(faculty_obj.user)
                # Notify Faculty about exam
                notification_type = 'specific'
                message = 'You have been selected as Exam coordinator for ' + exam_detail_obj.exam.exam_name + ' exam which is scheduled from ' + \
                          exam_detail_obj.schedule_start_date.__str__() + ' to ' + exam_detail_obj.schedule_end_date.__str__() + \
                          ' for subject ' + each_subject
                heading = 'Exam Schedule for ' + exam_detail_obj.exam.exam_name

                # year_branch_obj = exam_detail_obj.year
                # division = list(Division.objects.filter(is_active=True, year_branch=year_branch_obj))

                # Notify Exam co-ordinator
                notify_users(notification_type=notification_type, message=message, heading=heading,
                             users_obj=[each_exam_subject.coordinator.user],
                             user_type='faculty')

                return redirect('/')

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
    if has_role(user, 'student'):
        student_obj = user.student
        student_detail_obj = StudentDetail.objects.get(student=student_obj, is_active=True)
        year_branch_obj = student_detail_obj.batch.division.year_branch
        exam_objs = ExamDetail.objects.filter(is_active=True, year=year_branch_obj)
        exam_subjects = [list(each.examsubject_set.values_list('subject__short_form', flat=True)) for each in exam_objs]
        return render(request, 'view_exam.html', {
            'exams': exam_objs,
            'exam_subjects': exam_subjects
        })


def manage_exam(request):
    user = request.user
    class_active = "exam"
    if user.is_anonymous:
        return redirect('/login/')

    else:
        if has_role(user, 'faculty'):
            all_exams = ExamDetail.objects.all().order_by('-schedule_start_date')

            return render(request, 'manage_exam.html', {
                'class_active': class_active,
                'all_exams': all_exams
            })


def set_rooms(request):
    user = request.user
    if has_role(user, 'faculty'):
        if request.method == 'GET':
            all_exams = list(ExamDetail.objects.filter(is_active=True))
            done_exams = set([each.exam for each in ExamGroupDetail.objects.filter(is_active=True)])
            remaining = list(set(all_exams) - done_exams)
            print(remaining)
            branch_obj = Branch.objects.get(branch='Computer')
            available_rooms = Room.objects.filter(branch=branch_obj)
            return render(request, 'set_rooms.html', {
                'exams': remaining,
                'available_rooms': available_rooms
            })
        elif request.method == 'POST':
            all_exam_id = request.POST.getlist('exam')

            all_room_id = request.POST.getlist('room')



        else:
            return HttpResponse("Something went wrong")

    else:
        return HttpResponse('Access Denied')
