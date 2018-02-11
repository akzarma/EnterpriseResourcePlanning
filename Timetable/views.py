import json
from collections import OrderedDict

import firebase_admin
from django.http.response import HttpResponseRedirect
from firebase_admin import credentials, db
# from django.db.models import Q, datetime

import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User

from General.models import CollegeExtraDetail, BranchSubject, FacultySubject, CollegeYear, Batch, SemesterPeriod
from Registration.models import Branch, Subject, Faculty, Student
from Registration.models import Branch, Subject
from Timetable.tasks import save_timetable_celery
from .models import Time, Room, Timetable, DateTimetable
from Sync.function import write_to_firebase

import xlsxwriter


# save_timetable_celery()


# Create your views here.

def fill_timetable(request):
    times = []
    years = []
    # branch = Branch.objects.all()
    branch_obj = Branch.objects.get(branch='Computer')
    branch = branch_obj.branch
    for i in Time.objects.all().order_by('starting_time'):
        times.append(i.__str__())

    for i in CollegeYear.objects.all().order_by('year').values_list('year', flat=True).distinct():
        years.append(i)

    divisions = CollegeExtraDetail.objects.filter(branch=branch_obj).order_by('division').values_list('division',
                                                                                                      flat=True).distinct()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    # form = TimetableForm()
    # branch = Branch.objects.all().values_list('branch', flat=True)
    theory_room = [i.room_number for i in Room.objects.filter(branch=branch_obj, lab=False)]
    practical_room = [i.room_number for i in Room.objects.filter(branch=branch_obj, lab=True)]
    subjects_obj = BranchSubject.objects.filter(branch=branch_obj)
    subjects = []
    faculty = list(
        FacultySubject.objects.filter(division__in=CollegeExtraDetail.objects.filter(branch=branch_obj)).values_list(
            'faculty__initials', flat=True).distinct())
    divisions_js = ""
    for i in divisions:
        divisions_js += i

    # timetables = Timetable.objects.filter(is_practical=False)
    # timetable_prac = Timetable.objects.filter(is_practical=True)
    subjects_json = {}
    all_subjects = BranchSubject.objects.filter(branch=branch_obj)
    for year in years:
        subjects = all_subjects.filter(year=CollegeYear.objects.get(year=year))
        subjects_theory = list(subjects.filter(subject__is_practical=False).values_list(
            'subject__short_form', flat=True))
        subjects_practical = list(subjects.filter(subject__is_practical=True).values_list(
            'subject__short_form', flat=True))
        subjects_json[year] = {
            'theory': subjects_theory,
            'practical': subjects_practical
        }

    # Create dict of subject teacher binding
    # eg
    # TOC:{
    #     A:[DMV,HVD]
    #     B:[DV]
    #     C:[]
    # }

    subject_teacher_json = {}

    for each_subject in all_subjects:

        subject_teacher_json[each_subject.subject.short_form] = {}
        for each_division in divisions:
            division_object = CollegeExtraDetail.objects.get(branch=branch_obj, division=each_division,
                                                             year=each_subject.year)
            faculty_subjects_division = FacultySubject.objects.filter(subject=each_subject.subject,
                                                                      division=division_object).values_list(
                'faculty__initials', flat=True)

            subject_teacher_json[each_subject.subject.short_form][each_division] = list(faculty_subjects_division)

    all_subjects = list(all_subjects.values_list('subject__short_form', flat=True))

    subject_year = {}

    # for year in years:

    batches_json = {}

    college_extra_details_obj = CollegeExtraDetail.objects.filter(branch=branch_obj)

    for yr in college_extra_details_obj:

        if yr.year.year in batches_json:
            batches_json[yr.year.year][yr.division] = list(
                Batch.objects.filter(division=yr).values_list('batch_name', flat=True))
        else:
            batches_json[yr.year.year] = {}
            batches_json[yr.year.year][yr.division] = list(
                Batch.objects.filter(division=yr).values_list('batch_name', flat=True))
        # for div in divisions:
        #     batches_json[yr][div] = [
        #         Batch.objects.filter(division=CollegeExtraDetail.objects.get(branch=branch_obj, division=div,
        #                                                                      year=CollegeYear.objects.get(
        #                                                                          year=yr))).values_list('batch_name',
        #                                                                                                 flat=True)
        #     ]

    full_timetable_theory = Timetable.objects.filter(branch_subject__branch=branch_obj, is_practical=False)
    full_timetable_practical = Timetable.objects.filter(branch_subject__branch=branch_obj, is_practical=True)

    timetable_instance = {}
    timetable_instance_practical = {}

    for each_time_table in full_timetable_theory:
        timetable_instance[
            'id_room_' + each_time_table.time.__str__() + '_' + each_time_table.division.division + '_' + str(
                days.index(each_time_table.day) + 2) + '_' + each_time_table.division.year.year + '_cbx'] = {
            'faculty': each_time_table.faculty.initials,
            'room': each_time_table.room.room_number,
            'subject': each_time_table.branch_subject.subject.short_form,
            'is_practical': 'false'
        }

    for each_time_table in full_timetable_practical:
        timetable_instance_practical[
            'id_room_' + each_time_table.time.__str__() + '_' + each_time_table.division.division + '_' + str(
                days.index(each_time_table.day) + 2) + '_' + each_time_table.division.year.year + '_' +
            each_time_table.batch.batch_name + '_cbx'] = {
            'faculty': each_time_table.faculty.initials,
            'room': each_time_table.room.room_number,
            'subject': each_time_table.branch_subject.subject.short_form,
            'is_practical': 'true'
        }

    context = {
        'branch': branch,
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
        'all_subjects': all_subjects,
        'subject_teacher_json': json.dumps(subject_teacher_json),
        'timetable_instance_theory': timetable_instance,
        'timetable_instance_practical': timetable_instance_practical
    }
    return render(request, 'test_timetable.html', context)


def fill_date_timetable():
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    start_date = SemesterPeriod.objects.all()[0].start_date
    end_date = SemesterPeriod.objects.all()[0].end_date
    date_range = (end_date - start_date).days + 1
    all_timetable = Timetable.objects.all()
    for date in (start_date + datetime.timedelta(n) for n in range(date_range)):
        for each in all_timetable:
            if days[date.weekday()] == each.day:
                DateTimetable.objects.create(date=date, original=each, is_substituted=False)

    return


def save_timetable(request):
    if request.method == "POST":

        save_timetable_celery.delay(request.POST)
        to_json()
        return HttpResponse('asdkasjb')
    else:
        return HttpResponse("Not Post")


def to_json():
    branch_obj = Branch.objects.get(branch='Computer')
    full_timetable = Timetable.objects.filter(branch_subject__branch=branch_obj)

    answer = {}
    faculty_json = {}
    for each in full_timetable:
        year = each.branch_subject.year.year
        branch = each.branch_subject.branch.branch

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

        if faculty in faculty_json:
            if day in faculty_json[faculty]:
                if time in faculty_json[faculty][day]:
                    var = {}
                else:
                    faculty_json[faculty][day][time] = {}

            else:
                faculty_json[faculty][day] = {}
                faculty_json[faculty][day][time] = {}

        else:
            faculty_json[faculty] = {}
            faculty_json[faculty][day] = {}
            faculty_json[faculty][day][time] = {}

        is_practical = each.is_practical

        if is_practical:
            batch = each.batch.batch_name
            if 'is_practical' in answer[year][branch][division][day][time]:
                print('contains')
            else:
                answer[year][branch][division][day][time] = {
                    'is_practical': is_practical
                }
            answer[year][branch][division][day][time][batch] = {
                'faculty': faculty,
                'room': room,
                'subject': subject,
            }
            faculty_json[faculty][day][time] = {
                'branch': branch,
                'division': division,
                'room': room,
                'subject': subject,
                'year': year,
                'batch': batch
            }
        else:
            answer[year][branch][division][day][time] = {
                'faculty': faculty,
                'room': room,
                'subject': subject,
                'is_practical': is_practical
            }

            faculty_json[faculty][day][time] = {
                'branch': branch,
                'division': division,
                'room': room,
                'subject': subject,
                'year': year
            }

    write_to_firebase(answer, 'Student')
    write_to_firebase(faculty_json, 'Faculty')



