import json
from collections import OrderedDict

import datetime
from ipaddress import collapse_addresses

# import firebase_admin
from celery import current_app
from celery.task import task
from django.db.models import Q
from django.http.response import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
# from firebase_admin import credentials, db

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from General.models import Division, BranchSubject, FacultySubject, CollegeYear, Batch, \
    StudentDetail, Semester, YearBranch, YearSemester, ElectiveDivision, StudentSubject
from Registration.models import Branch, Subject, Faculty, Student, ElectiveSubject
from Registration.models import Branch, Subject
from Registration.views import has_role
from Roles.models import RoleManager
from .models import Time, Room, Timetable, DateTimetable
# from Sync.function import write_to_firebase

import xlsxwriter


# Create your views here.

def fill_timetable(request):
    user = request.user
    if not user.is_anonymous:
        is_faculty = RoleManager.objects.filter()
        if is_faculty:
            # Default branch Computer and default semester 2
            current_semester = 2
            current_branch = 'Computer'
            if request.method == "POST":
                current_semester = int(request.POST.get('current_semester'))
                current_branch = request.POST.get('current_branch')
            branch_obj = Branch.objects.get(branch=current_branch)
            semester_obj = Semester.objects.get(semester=current_semester, is_active=True)
            times = []
            years = []
            all_branch = Branch.objects.all().values_list('branch', flat=True)
            year_branch_obj = YearBranch.objects.filter(branch=branch_obj)
            branch = branch_obj.branch
            for i in Time.objects.all().order_by('starting_time'):
                times.append(i.__str__())

            for i in CollegeYear.objects.all().order_by('year').values_list('year', flat=True).distinct():
                years.append(i)

            year_semester_json = {}
            for obj in YearSemester.objects.filter(is_active=True, semester__is_active=True,
                                                   year_branch__in=year_branch_obj):
                year_sem = obj.year_branch.year.year
                semester = obj.semester.semester
                if year_sem not in year_semester_json:
                    year_semester_json[year_sem] = []
                year_semester_json[year_sem] += [semester]

            divisions = Division.objects.filter(year_branch__in=year_branch_obj, is_active=True).order_by(
                'division').values_list(
                'division',
                flat=True).distinct()
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
            # form = TimetableForm()
            # branch = Branch.objects.all().values_list('branch', flat=True)
            theory_room = [i.room_number for i in Room.objects.filter(branch=branch_obj, lab=False)]
            practical_room = [i.room_number for i in Room.objects.filter(branch=branch_obj, lab=True)]
            # college_detail = Division.objects.filter(year_branch__in=year_branch_obj)
            # subjects_obj = BranchSubject.objects.filter(year_branch=college_detail[0])
            subjects = []
            faculty = list(
                FacultySubject.objects.filter(
                    division__in=Division.objects.filter(year_branch__in=year_branch_obj)).values_list(
                    'faculty__initials', flat=True).distinct())
            divisions_js = ""
            for i in divisions:
                divisions_js += i
            # timetables = Timetable.objects.filter(is_practical=False)
            # timetable_prac = Timetable.objects.filter(is_practical=True)
            subjects_json = {}
            # college_detail = CollegeExtraDetail.objects.filter(year_branch__in=year_branch_obj)
            all_subjects = BranchSubject.objects.filter(year_branch__in=year_branch_obj, semester=semester_obj)

            for year in years:
                year_obj = CollegeYear.objects.get(year=year)
                # college_detail = CollegeExtraDetail.objects.filter(year_branch__in=YearBranch.objects.filter(year=year_obj))
                year_branch_objs = YearBranch.objects.filter(year=year_obj)
                subjects = all_subjects.filter(year_branch__in=year_branch_objs)
                subjects_theory = list(
                    subjects.filter(subject__is_practical=False, subject__is_elective_group=False).values_list(
                        'subject__short_form', flat=True))
                subjects_practical = list(
                    subjects.filter(subject__is_practical=True, subject__is_elective_group=False).values_list(
                        'subject__short_form', flat=True))
                subjects_elective_theory = list(
                    subjects.filter(subject__is_elective_group=True, subject__is_practical=False))
                subjects_elective_practical = list(
                    subjects.filter(subject__is_elective_group=True, subject__is_practical=True))
                subjects_json[year] = {
                    'theory': subjects_theory,
                    'practical': subjects_practical,
                    'elective_theory': {},
                    'elective_practical': {}
                }
                for each_elective_theory in subjects_elective_theory:
                    subjects_json[year]['elective_theory'][each_elective_theory.subject.short_form] = {}
                    # a = each_elective_theory.subject.electivesubject_set
                    for each_option in each_elective_theory.subject.electivesubject_set.all():
                        a = each_option.electivedivision_set.filter(is_active=True).values_list(
                            'elective_subject__short_form', flat=True)
                        subjects_json[year]['elective_theory'][each_elective_theory.subject.short_form][
                            each_option.short_form] = [
                            list(each_option.electivedivision_set.filter(is_active=True).values_list(
                                'division', flat=True))]

                for each_elective_practical in subjects_elective_practical:
                    subjects_json[year]['elective_practical'][each_elective_practical.subject.short_form] = {}
                    # a = each_elective_theory.subject.electivesubject_set
                    for each_option in each_elective_practical.subject.electivesubject_set.all():
                        subjects_json[year]['elective_practical'][each_elective_practical.subject.short_form][
                            each_option.short_form] = [
                            list(each_option.electivedivision_set.filter(is_active=True).values_list(
                                'elective_subject__short_form', flat=True))]

            # Create dict of subject teacher binding
            # eg
            # TOC:{
            #     A:[DMV,HVD]
            #     B:[DV]
            #     C:[]
            # }
            non_elective_subjects = all_subjects.filter(subject__is_elective_group=False)
            elective_subjects = all_subjects.filter(subject__is_elective_group=True)
            subject_teacher_json = {}

            for each_subject in non_elective_subjects:
                subject_teacher_json[each_subject.subject.short_form] = {}
                for each_division in divisions:
                    division_object = Division.objects.get(year_branch=each_subject.year_branch, division=each_division)
                    faculty_subjects_division = FacultySubject.objects.filter(subject=each_subject.subject,
                                                                              division=division_object).values_list(
                        'faculty__initials', flat=True)

                    subject_teacher_json[each_subject.subject.short_form][each_division] = list(
                        faculty_subjects_division)

            elective_subject_teacher_json = {}

            # eg
            # {
            #     EL1: {
            #         ML: {
            #             1:[APK, PVK]
            #
            #         }
            #         DM: {
            #
            #         }
            #     }
            # }
            for each_subject in elective_subjects:
                elective_subject_teacher_json[each_subject.subject.short_form] = {}

                elective_option = each_subject.subject.electivesubject_set.all()

                for each_option in elective_option:
                    elective_subject_teacher_json[each_subject.subject.short_form][each_option.short_form] = {}

                    division_elective = each_option.electivedivision_set.filter(is_active=True)

                    for each_division in division_elective:
                        elective_subject_teacher_json[each_subject.subject.short_form][each_option.short_form][
                            each_division.division] = list(FacultySubject.objects.filter(is_active=True,
                                                                                         subject=each_subject.subject,
                                                                                         elective_subject=each_option,
                                                                                         elective_division=each_division).values_list(
                            'faculty__initials', flat=True))

            all_subjects = list(all_subjects.values_list('subject__short_form', flat=True))

            subject_year = {}

            # for year in years:

            batches_json = {}

            year_branch_objs = YearBranch.objects.filter(branch=branch_obj)
            division_obj = Division.objects.filter(year_branch__in=year_branch_objs)

            for yr in division_obj:

                if yr.year_branch.year.year in batches_json:
                    batches_json[yr.year_branch.year.year][yr.division] = list(
                        Batch.objects.filter(division=yr).values_list('batch_name', flat=True))
                else:
                    batches_json[yr.year_branch.year.year] = {}
                    batches_json[yr.year_branch.year.year][yr.division] = list(
                        Batch.objects.filter(division=yr).values_list('batch_name', flat=True))
                # for div in divisions:
                #     batches_json[yr][div] = [
                #         Batch.objects.filter(division=CollegeExtraDetail.objects.get(branch=branch_obj, division=div,
                #                                                                      year=CollegeYear.objects.get(
                #                                                                          year=yr))).values_list('batch_name',
                #                                                                                                 flat=True)
                #

            full_timetable_theory = Timetable.objects.filter(branch_subject__year_branch__branch=branch_obj,
                                                             branch_subject__semester=semester_obj, is_practical=False,
                                                             branch_subject__subject__is_elective_group=False)
            full_timetable_practical = Timetable.objects.filter(branch_subject__year_branch__branch=branch_obj,
                                                                branch_subject__semester=semester_obj,
                                                                is_practical=True)

            full_timetable_elective = Timetable.objects.filter(branch_subject__year_branch__branch=branch_obj,
                                                               branch_subject__semester=semester_obj,
                                                               branch_subject__subject__is_elective_group=True)

            timetable_instance = {}
            timetable_instance_practical = {}

            for each_time_table in full_timetable_theory:
                timetable_instance[
                    'id_room_' + each_time_table.time.__str__() + '_' + each_time_table.division.division + '_' + str(
                        days.index(
                            each_time_table.day) + 2) + '_' + each_time_table.division.year_branch.year.year + '_cbx'] = {
                    'faculty': each_time_table.faculty.initials,
                    'room': each_time_table.room.room_number,
                    'subject': each_time_table.branch_subject.subject.short_form,
                    'is_practical': 'false',
                    'is_elective': 'false'
                }

            for each_time_table in full_timetable_practical:
                timetable_instance_practical[
                    'id_room_' + each_time_table.time.__str__() + '_' + each_time_table.division.division + '_' + str(
                        days.index(
                            each_time_table.day) + 2) + '_' + each_time_table.division.year_branch.year.year + '_' +
                    each_time_table.batch.batch_name + '_cbx'] = {
                    'faculty': each_time_table.faculty.initials,
                    'room': each_time_table.room.room_number,
                    'subject': each_time_table.branch_subject.subject.short_form,
                    'is_practical': 'true',
                    'is_elective': 'false'
                }

            print(batches_json)

            context = {
                'branch': branch,
                'current_semester': current_semester,
                'times': times,
                'year': years,
                'days': days,
                'division': list(divisions),
                'number_of_division': range(len(divisions)),
                'theory_room': theory_room,
                'practical_room': practical_room,
                'batches_json': json.dumps(batches_json),
                'faculty': faculty,
                'divisions_js': divisions_js,
                'subject_json': json.dumps(subjects_json),
                'semester_json': year_semester_json,
                'all_subjects': all_subjects,
                'subject_teacher_json': json.dumps(subject_teacher_json),
                'timetable_instance_theory': timetable_instance,
                'timetable_instance_practical': timetable_instance_practical,
                'elective_subject_teacher_json': elective_subject_teacher_json,
                'all_branch': all_branch,
            }
            return render(request, 'test_timetable.html', context)
        return HttpResponseRedirect('/login/')
    return HttpResponseRedirect('/login/')


def fill_date_timetable(new_date_timetable, current_semester, current_branch):
    creation_list = []
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # Should always return 1 object
    DateTimetable.objects.all().update(is_active=False)
    branch_obj = Branch.objects.get(branch=current_branch)
    all_semester = Semester.objects.filter(semester=current_semester)
    all_years = CollegeYear.objects.all()  # FE ka dekhna hai
    for current_semester in all_semester:
        for year in all_years:
            print(branch_obj, year)
            year_branch_obj = YearBranch.objects.get(branch=branch_obj, year=year)
            year_semester_obj = YearSemester.objects.get(year_branch=year_branch_obj, semester=current_semester,
                                                         is_active=True)
            start_date = year_semester_obj.lecture_start_date
            end_date = year_semester_obj.lecture_end_date
            date_range = (end_date - start_date).days + 1
            for date in (start_date + datetime.timedelta(n) for n in range(date_range)):
                for each in new_date_timetable.filter(branch_subject__year_branch=year_branch_obj):
                    if days[date.weekday()] == each.day:
                        creation_list += [DateTimetable(date=date, original=each, is_substituted=False, is_active=True)]

    DateTimetable.objects.bulk_create(creation_list, batch_size=400)
    # return HttpResponse('DOne')


def save_timetable(request):
    if request.method == "POST":
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        current_branch = request.POST.get('current_branch')
        branch = Branch.objects.get(branch=current_branch)
        full_timetable = list(Timetable.objects.filter(branch_subject__year_branch__branch=branch))
        new_timetable = []
        for i in request.POST:

            if i.__contains__('_room_'):
                splitted = i.split('_room_')
                token = splitted[1].split('_')
                time = token[0].split('-')
                start_time = int(time[0].split(':')[0] + time[0].split(':')[1])
                end_time = int(time[1].split(':')[0] + time[1].split(':')[1])

                subject = splitted[0] + '_subject_' + splitted[1]
                day = days[int(token[2]) - 2]

                year = token[3]

                division = token[1]

                faculty_initials = request.POST.get(splitted[0] + '_teacher_' + splitted[1])

                room_number = request.POST.get(i)

                time = Time.objects.get(starting_time=start_time, ending_time=end_time)
                # day = day
                # subject = Subject.objects.get(
                #     short_form=subject_short_name)  # this has to be changed, should  not get subject with  short_name directly

                # branch = Branch.objects.get(branch='Computer')
                year_obj = CollegeYear.objects.get(year=year)
                year_branch_obj = YearBranch.objects.get(branch=branch, year=year_obj, is_active=True)
                subject_short_name = request.POST.get(subject)

                # room = Room.objects.get(room_number=room_number, branch=branch_subject.branch,lab=i)

                faculty = Faculty.objects.get(
                    initials=faculty_initials)  # this has to be changed, should not get only with initials. Use faculty_subject_set for that

                if len(token) < 5:  # theory (normal)
                    branch_subject = BranchSubject.objects.get(year_branch=year_branch_obj,
                                                               subject__short_form=subject_short_name, is_active=True)
                    division = Division.objects.get(division=division, year_branch=branch_subject.year_branch,
                                                    is_active=True)

                    timetable = Timetable.objects.filter(time=time, day=day, division=division,
                                                         is_practical=False)
                    room = Room.objects.get(room_number=room_number, branch=branch_subject.year_branch.branch,
                                            lab=False)

                    if timetable:
                        full_timetable.remove(timetable[0])
                        if not timetable[0].faculty == faculty:
                            timetable[0].faculty = faculty
                        if not timetable[0].branch_subject == branch_subject:
                            timetable[0].branch_subject = branch_subject
                        if not timetable[0].room == room:
                            timetable[0].room = room

                        timetable[0].save()
                    else:
                        timetable = Timetable(room=room, faculty=faculty, branch_subject=branch_subject, time=time,
                                              day=day, division=division,
                                              is_practical=False)

                        # timetable.save()
                        new_timetable += [timetable]
                elif len(token) < 6 and 'elective' in token:  # Elective theory

                    cbx_id = i + '_elective_cbx'

                    elective_subject = ElectiveSubject.objects.get()
                    elective_division = ElectiveDivision.objects.get(division=division,
                                                                     year_branch=branch_subject.year_branch,
                                                                     is_active=True)

                    timetable = Timetable.objects.filter(time=time, day=day, elective_division=elective_division,
                                                         is_practical=False)


                else:  # practical
                    branch_subject = BranchSubject.objects.get(year_branch=year_branch_obj,
                                                               subject__short_form=subject_short_name, is_active=True)
                    # batch = token[4]
                    division = Division.objects.get(division=division, year_branch=branch_subject.year_branch,
                                                    is_active=True)

                    batch = Batch.objects.get(division=division, batch_name=token[4])

                    timetable = Timetable.objects.filter(time=time, day=day, division=division,
                                                         is_practical=True,
                                                         batch=batch)
                    room = Room.objects.get(room_number=room_number, branch=branch_subject.year_branch.branch, lab=True)

                    if timetable:
                        full_timetable.remove(timetable[0])

                        if not timetable[0].faculty == faculty:
                            timetable[0].faculty = faculty
                        if not timetable[0].branch_subject == branch_subject:
                            timetable[0].branch_subject = branch_subject
                        if not timetable[0].room == room:
                            timetable[0].room = room

                        timetable[0].save()
                    else:
                        timetable = Timetable(room=room, faculty=faculty, branch_subject=branch_subject, time=time,
                                              day=day, division=division,
                                              is_practical=True, batch=batch)  # batch bhi add karna hai.

                        # timetable.save()
                        new_timetable += [timetable]

        Timetable.objects.bulk_create(new_timetable)

        # to_json(request)

        # Timetable.objects.filter(id__in=[i.id for i in full_timetable]).delete()

        # to_json()
        fill_date_timetable(Timetable.objects.all(), request.POST.get('current_semester'), current_branch)
        # get_excel(request)
        return HttpResponseRedirect('/timetable/enter/')
    else:
        return HttpResponse("Not Post")


# def to_json():
#     branch_obj = Branch.objects.get(branch='Computer')
#     full_timetable = Timetable.objects.filter(branch_subject__year_branch__branch=branch_obj)
#
#     answer = {}
#     faculty_json = {}
#     for each in full_timetable:
#         year = each.branch_subject.year_branch.year.year
#         branch = each.branch_subject.year_branch.branch.branch
#
#         division = each.division.division
#
#         day = each.day
#
#         time = each.time.format_for_json()
#
#         faculty = each.faculty.initials
#
#         room = each.room.room_number
#         subject = each.branch_subject.subject.short_form
#
#         if year in answer:
#             if branch in answer[year]:
#                 if division in answer[year][branch]:
#                     if day in answer[year][branch][division]:
#                         if time in answer[year][branch][division][day]:
#                             var = {}
#                         else:
#                             answer[year][branch][division][day][time] = {}
#                     else:
#                         answer[year][branch][division][day] = {}
#                         answer[year][branch][division][day][time] = {}
#
#                 else:
#                     answer[year][branch][division] = {}
#                     answer[year][branch][division][day] = {}
#                     answer[year][branch][division][day][time] = {}
#
#             else:
#                 answer[year][branch] = {}
#                 answer[year][branch][division] = {}
#                 answer[year][branch][division][day] = {}
#                 answer[year][branch][division][day][time] = {}
#         else:
#             answer[year] = {}
#             answer[year][branch] = {}
#             answer[year][branch][division] = {}
#             answer[year][branch][division][day] = {}
#             answer[year][branch][division][day][time] = {}
#
#         if faculty in faculty_json:
#             if day in faculty_json[faculty]:
#                 if time in faculty_json[faculty][day]:
#                     var = {}
#                 else:
#                     faculty_json[faculty][day][time] = {}
#
#             else:
#                 faculty_json[faculty][day] = {}
#                 faculty_json[faculty][day][time] = {}
#
#         else:
#             faculty_json[faculty] = {}
#             faculty_json[faculty][day] = {}
#             faculty_json[faculty][day][time] = {}
#
#         is_practical = each.is_practical
#
#         if is_practical:
#             batch = each.batch.batch_name
#             if 'is_practical' in answer[year][branch][division][day][time]:
#                 {}
#             else:
#                 answer[year][branch][division][day][time] = {
#                     'is_practical': is_practical
#                 }
#             answer[year][branch][division][day][time][batch] = {
#                 'faculty': faculty,
#                 'room': room,
#                 'subject': subject,
#             }
#             faculty_json[faculty][day][time] = {
#                 'branch': branch,
#                 'division': division,
#                 'room': room,
#                 'subject': subject,
#                 'year': year,
#                 'batch': batch
#             }
#         else:
#             answer[year][branch][division][day][time] = {
#                 'faculty': faculty,
#                 'room': room,
#                 'subject': subject,
#                 'is_practical': is_practical
#             }
#
#             faculty_json[faculty][day][time] = {
#                 'branch': branch,
#                 'division': division,
#                 'room': room,
#                 'subject': subject,
#                 'year': year
#             }
#
#     # write_to_firebase(answer, 'Student')
#     # write_to_firebase(faculty_json, 'Faculty')


def get_excel(request):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    branch_obj = Branch.objects.get(branch='Computer')
    full_timetable = Timetable.objects.filter(branch_subject__year_branch__branch=branch_obj)

    answer = OrderedDict()

    for each in sorted(full_timetable,
                       key=lambda x: (days.index(x.day), x.division.year_branch.year.number, x.time.starting_time)):
        year = each.branch_subject.year_branch.year.year
        branch = each.branch_subject.year_branch.branch.branch

        division = each.division.division

        day = each.day

        time = each.time

        faculty = each.faculty.initials

        room = each.room.room_number
        subject = each.branch_subject.subject.short_form

        if day in answer:
            if year in answer[day]:
                if division in answer[day][year]:
                    if time in answer[day][year][division]:
                        OrderedDict()
                    else:
                        answer[day][year][division][time] = OrderedDict()
                else:
                    answer[day][year][division] = OrderedDict()
                    answer[day][year][division][time] = OrderedDict()
            else:
                answer[day][year] = OrderedDict()
                answer[day][year][division] = OrderedDict()
                answer[day][year][division][time] = OrderedDict()
        else:
            answer[day] = OrderedDict()
            answer[day][year] = OrderedDict()
            answer[day][year][division] = OrderedDict()
            answer[day][year][division][time] = OrderedDict()

        is_practical = each.is_practical

        if is_practical:
            batch = each.batch.batch_name
            if 'is_practical' in answer[day][year][division][time]:
                {}
            else:
                answer[day][year][division][time] = {
                    'is_practical': is_practical
                }

            answer[day][year][division][time][batch] = {
                'faculty': faculty,
                'room': room,
                'subject': subject,
            }


        else:
            answer[day][year][division][time] = {
                'faculty': faculty,
                'room': room,
                'subject': subject,
                'is_practical': is_practical
            }

    answer = OrderedDict(sorted(answer.items(), key=lambda x: days.index(x[0])))

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('Expenses01.xlsx')
    worksheet = workbook.add_worksheet()

    col = 1

    year_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow'})

    subject_format = workbook.add_format({
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#f0bfff'})
    time_format = workbook.add_format({
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'color': 'red'})

    practical_format = workbook.add_format({
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#77abff'})

    full_time = [each.__str__() for each in sorted(Time.objects.all(), key=lambda x: x.starting_time)]

    for each_day in answer.items():

        merge_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'red'})

        row = 1
        temp = col

        # each_year_sorted = [each[0] for each in each_day[1].items()]

        for each_year in each_day[1].items():
            for each_division in each_year[1].items():
                worksheet.merge_range(row, temp, row, temp + 1, each_year[0] + each_division[0], year_format)

                each_division_sorted = OrderedDict(sorted(each_division[1].items(), key=lambda x: x[0].starting_time))
                row = 2
                temp_row = row
                for each_time in each_division_sorted.items():

                    temp_row = full_time.index(each_time[0].__str__()) * 8 + row

                    if not each_time[1]['is_practical']:
                        worksheet.merge_range(temp_row, temp, temp_row + 3, temp, str(each_time[1]['room']),
                                              subject_format)
                        worksheet.merge_range(temp_row, temp + 1, temp_row + 3, temp + 1, str(each_time[1]['faculty']),
                                              subject_format)

                        worksheet.merge_range(temp_row + 4, temp, temp_row + 7, temp + 1, each_time[1]['subject'],
                                              subject_format)
                        # temp_row += 8

                    else:
                        for each_key in sorted(each_time[1].keys()):
                            if not each_key == 'is_practical':
                                worksheet.write(temp_row, temp, each_key, practical_format)
                                worksheet.write(temp_row, temp + 1, each_time[1][each_key]['subject'], practical_format)
                                worksheet.write(temp_row + 1, temp, each_time[1][each_key]['room'], practical_format)
                                worksheet.write(temp_row + 1, temp + 1, each_time[1][each_key]['faculty'],
                                                practical_format)
                                temp_row += 2

                temp += 2
                row = 1

        row = 0
        worksheet.merge_range(0, col, 0, temp - 1, each_day[0], merge_format)
        col = temp

    row_offset = 2
    col_offset = 0

    row = 0
    col = 0

    worksheet.write(row, col, 'Time')

    for each_time in full_time:
        worksheet.merge_range(row + row_offset, col + col_offset, row + row_offset + 7, col + col_offset,
                              each_time, time_format)
        worksheet.set_column(col + col_offset, col + col_offset, len(str(each_time)))
        row += 8

    workbook.close()

    return HttpResponse('Done')


@csrf_exempt
def android_timetable_json(request):
    if request.method == 'POST':

        user_type = request.POST.get('user_type')
        print(user_type)
        if user_type == 'Student':
            answer = {}

            gr_number = request.POST.get('gr_number')

            if not gr_number:
                return HttpResponse('Error!')

            student = Student.objects.get(gr_number=gr_number)

            student_detail_obj = student.studentdetail_set.filter(is_active=True)

            if student_detail_obj.exists():

                if student_detail_obj.__len__() == 1:
                    student_detail_obj = student_detail_obj[0]

                    branch_obj = student_detail_obj.batch.division.year_branch.branch

                    college_extra_detail = StudentDetail.objects.get(student=student, is_active=True).batch.division

                    full_timetable = Timetable.objects.filter(branch_subject__year_branch__branch=branch_obj,
                                                              division=college_extra_detail)
                    # faculty_json = {}
                    for each in full_timetable:
                        year = each.branch_subject.year_branch.year.year
                        branch = each.branch_subject.year_branch.branch.branch

                        division = each.division.division

                        day = each.day

                        time = each.time.format_for_json()

                        faculty = each.faculty.initials

                        room = each.room.room_number
                        subject = each.branch_subject.subject.short_form

                        if year in answer:
                            if branch in answer[year]:
                                if division in answer[year][branch]:
                                    if day in answer[year][branch][division]:
                                        if time in answer[year][branch][division][day]:
                                            var = {}
                                        else:
                                            answer[year][branch][division][day][time] = {}
                                    else:
                                        answer[year][branch][division][day] = {}
                                        answer[year][branch][division][day][time] = {}

                                else:
                                    answer[year][branch][division] = {}
                                    answer[year][branch][division][day] = {}
                                    answer[year][branch][division][day][time] = {}

                            else:
                                answer[year][branch] = {}
                                answer[year][branch][division] = {}
                                answer[year][branch][division][day] = {}
                                answer[year][branch][division][day][time] = {}
                        else:
                            answer[year] = {}
                            answer[year][branch] = {}
                            answer[year][branch][division] = {}
                            answer[year][branch][division][day] = {}
                            answer[year][branch][division][day][time] = {}

                        is_practical = each.is_practical

                        if is_practical:
                            batch = each.batch.batch_name
                            if 'is_practical' in answer[year][branch][division][day][time]:
                                {}
                            else:
                                answer[year][branch][division][day][time] = {
                                    'is_practical': is_practical
                                }
                            answer[year][branch][division][day][time][batch] = {
                                'faculty': faculty,
                                'room': room,
                                'subject': subject,
                            }


                        else:
                            answer[year][branch][division][day][time] = {
                                'faculty': faculty,
                                'room': room,
                                'subject': subject,
                                'is_practical': is_practical
                            }

                    return JsonResponse(answer)
                else:
                    return JsonResponse({'error': 'Got more than 1 student object'})
            else:
                return JsonResponse({'error': 'Got no studentdetail object'})

        else:

            faculty_code = request.POST.get('faculty_code')
            print(request.POST)
            if not faculty_code:
                return HttpResponse('Error. no faculty code')

            faculty = Faculty.objects.get(faculty_code=faculty_code)

            full_timetable = DateTimetable.objects.filter(Q(original__faculty=faculty) | Q(substitute__faculty=faculty))
            faculty_json = {}
            for each in full_timetable:
                year = each.original.branch_subject.year_branch.year.year
                branch = each.original.branch_subject.year_branch.branch.branch

                division = each.original.division.division

                date = str(each.date.strftime('%d-%m-%Y'))

                time = each.original.time.format_for_json()

                faculty = each.original.faculty.initials

                room = each.original.room.room_number
                subject = each.original.branch_subject.subject.short_form

                if faculty in faculty_json:
                    if date in faculty_json[faculty]:
                        if time in faculty_json[faculty][date]:
                            var = {}
                        else:
                            faculty_json[faculty][date][time] = {}

                    else:
                        faculty_json[faculty][date] = {}
                        faculty_json[faculty][date][time] = {}

                else:
                    faculty_json[faculty] = {}
                    faculty_json[faculty][date] = {}
                    faculty_json[faculty][date][time] = {}

                is_practical = each.original.is_practical
                substitute = ''
                if each.is_substituted:
                    substitute = each.substitute.faculty.initials
                if is_practical:
                    batch = each.original.batch.batch_name

                    faculty_json[faculty][date][time] = {
                        'branch': branch,
                        'division': division,
                        'room': room,
                        'subject': subject,
                        'year': year,
                        'batch': batch,
                        'not_available': each.not_available,
                        'is_substituted': str(each.is_substituted),
                        'substitute': substitute
                    }
                else:

                    faculty_json[faculty][date][time] = {
                        'branch': branch,
                        'division': division,
                        'room': room,
                        'subject': subject,
                        'year': year,
                        'not_available': each.not_available,
                        'is_substituted': str(each.is_substituted),
                        'substitute': substitute
                    }
            print(JsonResponse(faculty_json))
            return JsonResponse(faculty_json)

    else:
        return HttpResponse('Error')


def register_time_slot(request):
    class_active = 'timetable'
    user = request.user
    if not user.is_anonymous:
        if has_role(user, 'faculty'):
            if request.method == "GET":
                return render(request, 'setup_time.html', {
                    'time_slots': Time.objects.all(),
                    'class_active': class_active
                })
            else:
                splitted_start_time = request.POST.get('start_time').split(':')
                splitted_end_time = request.POST.get('end_time').split(':')

                start_time = (int(splitted_start_time[0]) * 100) + int(splitted_start_time[1])
                end_time = (int(splitted_end_time[0]) * 100) + int(splitted_end_time[1])

                if len(Time.objects.filter(starting_time=start_time, ending_time=end_time)) > 0:
                    return render(request, 'setup_time.html', {
                        'error': 'Time slot already registered',
                        'time_slots': Time.objects.all(),
                        'class_active': class_active
                    })

                Time.objects.create(starting_time=start_time, ending_time=end_time)
                return render(request, 'setup_time.html', {
                    'success': 'Time slot registered',
                    'time_slots': Time.objects.all(),
                    'class_active': class_active
                })

        return redirect('/login/')
    return redirect('/login/')
