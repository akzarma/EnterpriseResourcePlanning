# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json

import os
from django.db.models import Avg, Sum, Count
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt

from General.models import CollegeYear, StudentDetail, BranchSubject, Batch, Division, StudentSubject
from Registration.forms import gr_roll_dict
from Registration.models import Student, Subject, Branch
from General.models import FacultySubject, StudentDetail
from Registration.models import Student, Subject, Faculty
from General.models import FacultySubject
from Registration.models import Student, Subject
from Registration.views import has_role
from Timetable.models import Timetable, DateTimetable, Time, Room
from Roles.models import RoleManager
from .models import StudentAttendance, SubjectLecture, StudentSubjectTotalAttendance


# Create your views here.
# def index(request):
#     user = request.user
#     if not user.is_anonymous:
#         if user.role == 'Faculty':
#             faculty = user.faculty
#             selected_class = request.POST.get('selected_class')
#             selected_class_obj = Timetable.objects.get(pk=selected_class)
#             selected_date = request.POST.get('selected_date')
#             selected_class_obj = DateTimetable.objects.get(date=parse_date(selected_date), original=selected_class_obj)
#             attendance = StudentAttendance.objects.filter(timetable=selected_class_obj).order_by('student__gr_number')
#             if attendance:
#                 all_students = attendance
#                 att = 1
#             else:
#                 all_students = StudentDivision.objects.filter(division=selected_class_obj.original.division) \
#                     .values_list('student', flat=True)
#                 all_students_roll = [StudentRollNumber.objects.get(student=each, is_active=True).roll_number for each in
#                                      all_students]
#                 sorted(all_students_roll)
#                 att = 0
#             timetables = faculty.timetable_set.all()
#             return render(request, "attendance.html", {
#                 'all_students': all_students,
#                 'selected_class': selected_class_obj,
#                 'faculty_subject': timetables,
#                 'att': att,
#                 'selected_date': selected_date
#             })
#
#
#         else:
#
#             # should be faculty....alert on login page with proper message.
#
#             return render(request, 'login.html', {'info': 'That page is only for Faculty'})
#     else:
#         return render(request, 'login.html', {'error': 'Login first'})


# def save(request):
#     user = request.user
#
#     if not user.is_anonymous:
#         if user.role == 'Faculty':
#             if request.method == 'POST':
#                 faculty = user.faculty
#                 present = request.POST.getlist('present')
#                 selected_date = request.POST.get('selected_date')
#
#                 timetable = Timetable.objects.get(pk=int(request.POST.get('selected_class')))
#                 division_obj = timetable.division
#                 all_students = StudentDivision.objects.filter(division=division_obj).values_list('student__pk',
#                                                                                                  flat=True)
#                 # all_students = StudentDetails.objects.all().values_list('pk', flat=True)
#                 absent = list(set(all_students) - set(present))
#
#                 whole = []
#                 for student in present:
#                     new = StudentAttendance.objects.filter(student=Student.objects.get(pk=student), timetable=timetable,
#                                                            date=parse_date(selected_date)).first()
#                     if new:
#                         new.attended = True
#                         new.save()
#                     else:
#                         new = StudentAttendance(student=Student.objects.get(pk=student), timetable=timetable,
#                                                 attended=True, date=parse_date(selected_date))
#                         whole.append(new)
#                 for student in absent:
#                     new = StudentAttendance.objects.filter(student=Student.objects.get(pk=student), timetable=timetable,
#                                                            date=parse_date(selected_date)).first()
#                     if new:
#                         new.attended = False
#                         new.save()
#                     else:
#                         new = StudentAttendance(student=Student.objects.get(pk=student), timetable=timetable,
#                                                 attended=False, date=parse_date(selected_date))
#                         whole.append(new)
#                 # StudentAttendance.objects.bulk_create(whole)
#                 StudentAttendance.objects.bulk_create(whole)
#
#                 faculty = user.faculty
#                 timetables = faculty.timetable_set.all()
#                 return render(request, 'select_cat.html', {'success': 'Attendance saved successfully',
#                                                            'faculty_subject': timetables})
#
#             else:
#                 return HttpResponseRedirect('/attendance/select')
#
#         else:
#             return HttpResponse('User not faculty')
#
#     else:
#         return HttpResponseRedirect('/login/')

def save(request):
    user = request.user

    if not user.is_anonymous:
        is_faculty = RoleManager.objects.filter(user=user, role__role='faculty')

        if is_faculty:
            faculty = user.faculty
            if 'save_attendance' in request.POST:
                selected_timetable = DateTimetable.objects.get(pk=request.POST.get('selected_timetable'))
                old_attendance_obj = StudentAttendance.objects.filter(timetable=selected_timetable)

                present_student_objs = list(StudentDetail.objects.filter(
                    roll_number__in=request.POST.getlist('present')))

                if not old_attendance_obj:
                    student_attendance = []

                    if not selected_timetable.is_substituted:
                        if selected_timetable.original.is_practical:
                            all_students = StudentDetail.objects.filter(
                                batch=selected_timetable.original.batch) \
                                .values_list('student', flat=True)
                        else:
                            all_students = StudentDetail.objects.filter(
                                batch__division=selected_timetable.original.division) \
                                .values_list('student', flat=True)

                        subject = selected_timetable.original.branch_subject.subject
                        subject_lecture = SubjectLecture.objects.get(
                            faculty_subject__faculty=selected_timetable.original.faculty,
                            faculty_subject__subject=subject,
                            faculty_subject__division=selected_timetable.original.division,
                        )

                        subject_lecture.conducted_lectures += 1

                    else:
                        if selected_timetable.substitute.is_practical:
                            all_students = StudentDetail.objects.filter(
                                batch=selected_timetable.substitute.batch) \
                                .values_list('student', flat=True)
                        else:
                            all_students = StudentDetail.objects.filter(
                                batch__division=selected_timetable.substitute.division) \
                                .values_list('student', flat=True)

                        subject_lecture = SubjectLecture.objects.get(
                            faculty_subject__faculty=selected_timetable.substitute.faculty,
                            faculty_subject__subject=selected_timetable.substitute.branch_subject.subject,
                            faculty_subject__division=selected_timetable.substitute.division,
                        )

                        subject = selected_timetable.substitute.branch_subject.subject

                        subject_lecture.conducted_lectures += 1

                    subject_lecture.save()

                    all_students_roll = [
                        StudentDetail.objects.get(student=each, is_active=True) for each in
                        all_students]

                    for roll in all_students_roll:
                        if roll in present_student_objs:
                            student_attendance += [
                                StudentAttendance(student=roll.student, timetable=selected_timetable,
                                                  attended=True)]

                            student_subject_total_attendance = StudentSubjectTotalAttendance.objects.get(
                                student=roll.student,
                                subject=subject)
                            student_subject_total_attendance \
                                .attended += 1
                            student_subject_total_attendance.save()


                        else:
                            student_attendance += [
                                StudentAttendance(student=roll.student, timetable=selected_timetable,
                                                  attended=False)]

                    StudentAttendance.objects.bulk_create(student_attendance)

                else:
                    for each in old_attendance_obj:
                        roll_number = StudentDetail.objects.get(student=each.student, is_active=True)
                        if roll_number in present_student_objs and each.attended is False:
                            each.attended = True
                            each.save()

                            if not selected_timetable.is_substituted:
                                student_subject_total_attendance = StudentSubjectTotalAttendance.objects.get(
                                    student=each.student,
                                    subject=selected_timetable.original.branch_subject.subject)
                                student_subject_total_attendance.attended += 1
                                student_subject_total_attendance.save()


                            else:
                                student_subject_total_attendance = StudentSubjectTotalAttendance.objects.get(
                                    student=each.student,
                                    subject=selected_timetable.substitute.branch_subject.subject)
                                student_subject_total_attendance.attended += 1
                                student_subject_total_attendance.save()

                        elif roll_number not in present_student_objs and each.attended is True:
                            each.attended = False
                            each.save()

                            if not selected_timetable.is_substituted:
                                student_subject_total_attendance = StudentSubjectTotalAttendance.objects.get(
                                    student=each.student,
                                    subject=selected_timetable.original.branch_subject.subject)
                                student_subject_total_attendance.attended -= 1
                                student_subject_total_attendance.save()

                            else:
                                student_subject_total_attendance = StudentSubjectTotalAttendance.objects.get(
                                    student=each.student,
                                    subject=selected_timetable.substitute.branch_subject.subject)
                                student_subject_total_attendance.attended -= 1
                                student_subject_total_attendance.save()

                timetable = sorted(
                    DateTimetable.objects.filter(date=selected_timetable.date, original__faculty=faculty),
                    key=lambda x: (x.date, x.original.time.starting_time))

                return render(request, 'dashboard_faculty.html', {'success': 'Attendance saved.',
                                                                  'selected_date': selected_timetable.date.strftime(
                                                                      '%d-%m-%Y'),
                                                                  'timetable': timetable})

    return render(request, 'dashboard_faculty.html', {'error': 'Some problem is there.'})


def select_cat(request):
    class_active = "attendance"
    user = request.user
    if not user.is_anonymous:
        is_faculty = RoleManager.objects.filter(user=user, role__role='faculty')
        # is_student = RoleManager.objects.filter(user=user, role__role='student')
        if is_faculty:
            if request.method == 'POST':
                faculty = user.faculty
                if 'GO' in request.POST:
                    selected_date = parse_date(request.POST.get('selected_date'))
                    timetable = sorted(
                        DateTimetable.objects.filter(date=selected_date, original__faculty=faculty),
                        key=lambda x: (x.date, x.original.time.starting_time))

                    return render(request, 'dashboard_faculty.html', {
                        'class_active': class_active,
                        'timetable': timetable,
                        'selected_date': selected_date,
                    })

                elif 'date_timetable' in request.POST:
                    selected_date = parse_date(request.POST.get('selected_date'))
                    timetable = sorted(
                        DateTimetable.objects.filter(date=selected_date, original__faculty=faculty),
                        key=lambda x: (x.date, x.original.time.starting_time))

                    selected_class_obj = DateTimetable.objects.get(pk=request.POST.get('date_timetable'))

                    if selected_class_obj.original.is_practical:
                        attendance = StudentAttendance.objects.filter(
                            student__studentdetail__batch=selected_class_obj.original.batch,
                            timetable=selected_class_obj)

                        present_roll = sorted(
                            [StudentDetail.objects.get(student=each.student).roll_number for each in attendance if
                             each.attended is True])

                        all_students = StudentDetail.objects.filter(
                            batch=selected_class_obj.original.batch).values_list('student', flat=True)
                        all_students_roll = sorted(
                            [StudentDetail.objects.get(student=each, is_active=True).roll_number for
                             each in all_students])

                    else:
                        attendance = StudentAttendance.objects.filter(timetable=selected_class_obj)
                        present_roll = sorted([StudentDetail.objects.get(student=each.student).roll_number
                                               for each in attendance if each.attended is True])

                        all_students = StudentDetail.objects.filter(
                            batch__division=selected_class_obj.original.division) \
                            .values_list('student', flat=True)
                        all_students_roll = sorted(
                            [StudentDetail.objects.get(student=each, is_active=True).roll_number for
                             each in all_students])

                    if attendance:
                        att = 1

                    else:
                        att = 0

                    return render(request, 'dashboard_faculty.html', {
                        'class_active': class_active,
                        'timetable': timetable,
                        'selected_date': selected_date,
                        'att': att,
                        'selected_timetable': selected_class_obj,
                        'all_students_roll': all_students_roll,
                        'present_roll': present_roll,
                    })

            else:
                return render(request, 'select_cat.html', {
                    'class_active': class_active,
                })

        else:
            # should be faculty....alert on login page with proper message.
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')


# def check_attendance(request):
#     user = request.user
#     if not user.is_anonymous:
#         if user.role == 'Faculty':
#             if request.method == 'POST':
#                 if request.POST.get('go'):
#                     selected_date = request.POST.get('selected_date')
#                     current_tt = request.POST.get('selected_class')
#                     current_tt_obj = Timetable.objects.get(pk=current_tt)
#                     count = 0
#                     present_percent = 0
#                     all_students = StudentAttendance.objects.filter(timetable=current_tt_obj,
#                                                                     date=parse_date(selected_date)).order_by(
#                         'student__gr_number')
#                     count = all_students.filter(attended=True).count()
#
#                     if all_students.count():
#                         present_percent = count / all_students.count()
#                     return render(request, "check_attendance.html", {
#                         'all_students': all_students,
#                         'present': present_percent * 100
#                     })
#
#                 elif request.POST.get('check_attendance_button'):
#                     selected_from_date = request.POST.get('selected_from_date')
#                     selected_to_date = request.POST.get('selected_to_date')
#                     selected_faculty_subject = request.POST.get('selected_subject')
#                     selected_faculty_subject_obj = FacultySubject.objects.get(pk=selected_faculty_subject)
#                     branch_subject_obj = BranchSubject.objects.get(subject=selected_faculty_subject_obj.subject,
#                                                                    branch=selected_faculty_subject_obj.division.branch,
#                                                                    year=selected_faculty_subject_obj.division.year,
#                                                                    semester=1)
#                     #
#                     # Semester ko subject se lena hai
#                     #
#                     current_tt_obj = Timetable.objects.filter(faculty=selected_faculty_subject_obj.faculty,
#                                                               division=selected_faculty_subject_obj.division,
#                                                               branch_subject=branch_subject_obj)
#
#                     lecture_percentage = 0
#                     all_students_count = 0
#                     all_students_present = 0
#                     individual_attendance = {}
#
#                     for i in StudentDetail.objects.filter(
#                             division__branch=selected_faculty_subject_obj.division.branch,
#                             division__year=selected_faculty_subject_obj.division.year,
#                             division__division=selected_faculty_subject_obj.division.division,
#                             division__shift=selected_faculty_subject_obj.division.shift):
#                         individual_attendance[i.student.pk] = 0
#
#                     count_present = 0
#                     for i in current_tt_obj:  # For days in week
#                         all_students_obj = StudentAttendance.objects.filter(timetable=i, date__range=(
#                             selected_from_date, selected_to_date))  # For the day in every week in given date range
#                         all_students_count += all_students_obj.count()
#                         all_students_present += all_students_obj.filter(attended=True).count()
#
#                         for j in all_students_obj:
#                             if j.attended:
#                                 individual_attendance[j.student.pk] += 1
#
#                     if all_students_count:
#                         lecture_percentage += all_students_present / all_students_count * 100
#
#                     return render(request, 'lecture_attendance.html',
#                                   {'lecture_percent': "{0:.2f}".format(lecture_percentage),
#                                    'selected_from_date': selected_from_date,
#                                    'selected_to_date': selected_to_date,
#                                    'individual_attendance': individual_attendance})
#
#             elif request.method == "GET":
#                 faculty = user.faculty
#                 timetables = faculty.timetable_set.all()
#                 faculty_subject = FacultySubject.objects.filter(faculty=faculty)
#                 return render(request, 'select_check_attendance.html',
#                               {'faculty_subject': timetables, 'subjects': faculty_subject})
#         else:
#             return HttpResponseRedirect('/login/')
#     else:
#         return HttpResponseRedirect('/login/')


@csrf_exempt
def android_display_attendance(request):
    if request.method == 'POST':
        gr_number = request.POST.get('gr_number')

        if not gr_number:
            error = {
                'error': 'No GR number.'
            }
            return HttpResponse(error)

        student = Student.objects.get(gr_number=gr_number)

        total_attendance = student.totalattendance_set.all()

        response = {}

        attended = 0
        total = 0

        for each in total_attendance:
            total += each.total_lectures
            attended += each.attended_lectures
            response[each.subject.short_form] = {
                'total': each.total_lectures,
                'attended': each.attended_lectures
            }
        total_percent = round(100 * attended / total, 2) if total is not 0 else 0

        response['total_percent'] = str(total_percent) + '%'
        return JsonResponse(response)

    else:
        error = {
            'error': 'Not Post.'
        }
        return HttpResponse(error)


def mark_from_excel(request):
    cwd = os.getcwd()
    app_name = '/EnterpriseResourcePlanning'
    if cwd.__contains__(app_name):
        path = cwd + '/Attendance/Documents/TE_B_attendance.csv'
    else:
        path = cwd + app_name + '/Attendance/Documents/TE_B_attendance.csv'

    new = []
    file = open(path, 'r')

    full_text = file.read()

    each_line = full_text.split('\n')

    subjects = each_line[0].split(',')

    each_line.remove(each_line[0])
    each_line.remove(each_line[0])

    for each_student in each_line:

        token = each_student.split(',')
        roll = int(token[0])

        student = StudentDetail.objects.filter(roll_number=roll)

        if student:
            student = student[0].student
            for (each_subject, i) in zip(subjects, range(5)):

                lect = token[i + 2]

                lect_split = lect.split('/')

                attended = 0
                total = 0

                # print(lect_split)
                if lect_split.__len__() != 1:
                    attended = int(lect_split[0].strip())
                    total = int(lect_split[1].strip())

                subject_obj = Subject.objects.get(code=each_subject)

                totalAttendance = TotalAttendance.objects.filter(student=student, subject=subject_obj)
                if not totalAttendance:
                    TotalAttendance.objects.create(student=student, subject=subject_obj, total_lectures=total,
                                                   attended_lectures=attended)
                    try:
                        new.append(
                            student.gr_number + " " + student.first_name + " " + str(
                                student.studentdetail_set.first().roll_number))
                    except:
                        pass
                else:
                    totalAttendance[0].total_lectures = total
                    totalAttendance[0].attended_lectures = attended
                    totalAttendance[0].save()



        else:
            pass

    return HttpResponse("Done new: " + str(new))


@csrf_exempt
def android_fill_attendance(request):
    if request.method == "POST":
        for each in request.POST:
            if each.__contains__('attendance_'):
                attendance_json = json.loads(request.POST.get(each))
                timetable_type = 'original'
                time_obj = Time.objects.get(starting_time=int(attendance_json['start_time']),
                                            ending_time=int(attendance_json['end_time']))
                branch_obj = Branch.objects.get(branch=attendance_json['branch'])
                room_obj = Room.objects.get(branch=branch_obj, room_number=attendance_json['room'])
                faculty = Faculty.objects.get(faculty_code=attendance_json['faculty_code'])
                year_obj = CollegeYear.objects.get(year=attendance_json['year'])
                subject_obj = Subject.objects.get(short_form=attendance_json['subject'])
                division_obj = Division.objects.get(year_branch__branch=branch_obj, year_branch__year=year_obj,
                                                    division=attendance_json['division'])
                # college_detail = Division.objects.filter(branch=branch_obj, year=year_obj)
                branch_subject = BranchSubject.objects.get(year_semester__year_branch__branch=branch_obj,
                                                           year_semester__year_branch__year=year_obj
                                                           , subject=subject_obj, year_semester__is_active=True)

                date = datetime.datetime.strptime(attendance_json['date'], '%Y,%m,%d').date()

                if attendance_json['is_practical'] is 'true':
                    batch = Batch.objects.get(division=division_obj, batch_name=attendance_json['batch'])
                    timetable_obj = Timetable.objects.get(room=room_obj, time=time_obj, day=attendance_json['day'],
                                                          faculty=faculty, division=division_obj,
                                                          branch_subject=branch_subject, is_practical=True, batch=batch)

                else:
                    timetable_obj = Timetable.objects.get(room=room_obj, time=time_obj, day=attendance_json['day'],
                                                          faculty=faculty, division=division_obj,
                                                          branch_subject=branch_subject)

                selected_timetable = DateTimetable.objects.filter(date=date, original=timetable_obj)
                if not selected_timetable.exists():
                    selected_timetable = DateTimetable.objects.filter(date=date, substitute=timetable_obj)
                    timetable_type = 'substitute'
                    if selected_timetable.exists():
                        selected_timetable = selected_timetable[0]
                    else:
                        return JsonResponse({
                            'error': "Timetable object not found"
                        })
                else:
                    selected_timetable = selected_timetable[0]

                if timetable_type == "original":
                    subject = selected_timetable.original.branch_subject.subject
                    subject_lecture = SubjectLecture.objects.get(
                        faculty_subject__faculty=selected_timetable.original.faculty,
                        faculty_subject__subject=subject,
                        faculty_subject__division=selected_timetable.original.division,
                    )

                else:
                    subject = selected_timetable.substitute.branch_subject.subject
                    subject_lecture = SubjectLecture.objects.get(
                        faculty_subject__faculty=selected_timetable.substitute.faculty,
                        faculty_subject__subject=subject,
                        faculty_subject__division=selected_timetable.substitute.division,
                    )

                subject_lecture.conducted_lectures += 1

                subject_lecture.save()

                attendance = []

                old_attendance_obj = StudentAttendance.objects.filter(timetable=selected_timetable)
                if not old_attendance_obj:
                    for roll_number in attendance_json['attendance']:
                        student = StudentDetail.objects.get(roll_number=roll_number, batch__division=division_obj,
                                                            is_active=True).student
                        attendance += [StudentAttendance(student=student, timetable=selected_timetable,
                                                         attended=bool(
                                                             attendance_json['attendance'][str(roll_number)]))]
                        student_subject_total_attendance = StudentSubjectTotalAttendance.objects.get(
                            student=student,
                            subject=subject)
                        student_subject_total_attendance \
                            .attended += 1
                        student_subject_total_attendance.save()

                    StudentAttendance.objects.bulk_create(attendance)

                else:
                    for i in old_attendance_obj:
                        roll_number = StudentDetail.objects.get(student=i.student, is_active=True).roll_number
                        i.attended = bool(attendance_json['attendance'][str(roll_number)])

                        if i.attended:
                            student_subject_total_attendance = StudentSubjectTotalAttendance.objects.get(
                                student=i.student,
                                subject=subject)
                            student_subject_total_attendance.attended += 1
                            student_subject_total_attendance.save()

                        else:
                            student_subject_total_attendance = StudentSubjectTotalAttendance.objects.get(
                                student=i.student,
                                subject=subject)
                            student_subject_total_attendance.attended -= 1
                            student_subject_total_attendance.save()

                        i.save()
        print('Done android')
        return HttpResponse('true')

    else:
        print('error_android')
        return HttpResponse('ERROR')


def reload_student_roll(request):
    # students = Student.objects.all()
    # for each_student in students:
    #     studentRollNumber = StudentRollNumber.objects.filter(student=each_student)
    #     if not studentRollNumber:
    #         StudentRollNumber.objects.create(student=each_student, roll_number=
    #         [gr_roll_dict[i] for i in gr_roll_dict if i == each_student.gr_number][0])

    return HttpResponse("not ok")


@csrf_exempt
def android_instance(request):
    if request.method == "POST":
        print(request.POST)
        timetable_json = json.loads(request.POST.get('I_WANT_THE_INSTANCE_BRUV'))
        time_obj = Time.objects.get(starting_time=int(timetable_json['start_time']),
                                    ending_time=int(timetable_json['end_time']))

        branch_obj = Branch.objects.get(branch=timetable_json['branch'])
        room_obj = Room.objects.get(branch=branch_obj, room_number=timetable_json['room'])
        faculty = Faculty.objects.get(faculty_code=timetable_json['faculty_code'])
        year_obj = CollegeYear.objects.get(year=timetable_json['year'])
        subject_obj = Subject.objects.get(short_form=timetable_json['subject'])
        division_obj = Division.objects.get(year_branch__branch=branch_obj, year_branch__year=year_obj,
                                            division=timetable_json['division'])
        # college_detail = Division.objects.filter(branch=branch_obj, year=year_obj)
        branch_subject = BranchSubject.objects.get(year_semester__year_branch__branch=branch_obj, year_semester__year_branch__year=year_obj,
                                                   subject=subject_obj)

        date = datetime.datetime.strptime(timetable_json['date'], '%Y,%m,%d').date()

        if timetable_json['is_practical'] is 'true':
            batch = Batch.objects.get(division=division_obj, batch_name=timetable_json['batch'])
            timetable_obj = Timetable.objects.get(room=room_obj, time=time_obj, day=timetable_json['day'],
                                                  faculty=faculty, division=division_obj,
                                                  branch_subject=branch_subject, is_practical=True, batch=batch)
            selected_timetable = DateTimetable.objects.get(date=date, original=timetable_obj)

        else:
            timetable_obj = Timetable.objects.get(room=room_obj, time=time_obj, day=timetable_json['day'],
                                                  faculty=faculty, division=division_obj,
                                                  branch_subject=branch_subject)
            selected_timetable = DateTimetable.objects.get(date=date, original=timetable_obj)

        response = {}

        for i in StudentAttendance.objects.filter(timetable=selected_timetable):
            response[StudentDetail.objects.get(student=i.student).roll_number] = 1 if i.attended else 0

        if bool(response):
            return HttpResponse(json.dumps(response))
        else:
            return HttpResponse('No instance found')

    else:
        return HttpResponse('ERROR')


def subject_attendance(request):
    user = request.user

    if user.is_anonymous:
        return redirect('/login/')
    if has_role(user, 'faculty'):
        faculty_obj = user.faculty

        if request.method == 'GET':

            subject_json = {}

            subject_objs = [each.subject for each in FacultySubject.objects.filter(faculty=faculty_obj, is_active=True)]
            for each_subject in subject_objs:
                branch_subject = BranchSubject.objects.get(subject=each_subject, is_active=True)
                year = branch_subject.year_branch.year.year
                branch = branch_subject.year_branch.branch.branch

                if branch in subject_json:
                    if year in subject_json[branch]:
                        subject_json[branch][year].append(each_subject)
                    else:
                        subject_json[branch][year] = []
                else:
                    subject_json[branch] = {}

            return render(request, )

        elif request.method == 'POST':
            pass

            subjects = request.POST.getlist('subject')
            for each_subject in subjects:
                subject_obj = Subject.objects.get(is_active=True, short_form=each_subject)
                StudentSubject.objects.filter(subject)
