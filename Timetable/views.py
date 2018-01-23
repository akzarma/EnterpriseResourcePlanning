import json
from collections import defaultdict

import firebase_admin
from django.http.response import HttpResponseRedirect
from firebase_admin import credentials, db
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from scipy.constants import year

from General.models import CollegeExtraDetail, BranchSubject, FacultySubject, CollegeYear, Batch
# from .forms import TimetableForm
from Registration.models import Branch, Subject, Faculty, Student
from .models import Time, Room, Timetable
from Registration.models import Branch, Subject
from .models import Time, Room, Timetable
import copy
from Sync.function import write_to_firebase

import xlsxwriter


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


def save_timetable(request):
    if request.method == "POST":
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        for i in request.POST:
            if i.__contains__('_room_'):
                splitted = i.split('_room_')
                token = splitted[1].split('_')
                time = token[0].split('-')
                start_time = int(time[0].split(':')[0] + time[0].split(':')[1])
                end_time = int(time[1].split(':')[0] + time[1].split(':')[1])

                subject = splitted[0] + '_subject_' + splitted[1]
                subject_short_name = request.POST.get(subject)

                division = token[1]

                day = days[int(token[2]) - 2]

                year = token[3]

                faculty_initials = request.POST.get(splitted[0] + '_teacher_' + splitted[1])

                room_number = request.POST.get(i)

                time = Time.objects.get(starting_time=start_time, ending_time=end_time)
                # day = day
                # subject = Subject.objects.get(
                #     short_form=subject_short_name)  # this has to be changed, should  not get subject with  short_name directly

                branch = Branch.objects.get(branch='Computer')
                year = CollegeYear.objects.get(year=year)
                branch_subject = BranchSubject.objects.get(branch=branch, year=year,
                                                           subject__short_form=subject_short_name)
                room = Room.objects.get(room_number=room_number, branch=branch_subject.branch)

                faculty = Faculty.objects.get(
                    initials=faculty_initials)  # this has to be changed, should not get only with initials. Use faculty_subject_set for that

                division = CollegeExtraDetail.objects.get(division=division, branch=branch_subject.branch,
                                                          year=branch_subject.year
                                                          )

                if len(token) < 5:  # theory
                    timetable = Timetable.objects.filter(time=time, day=day, division=division,
                                                         is_practical=False)

                    if timetable:
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

                        timetable.save()

                else:  # practical
                    # batch = token[4]
                    batch = Batch.objects.get(division=division, batch_name=token[4])

                    timetable = Timetable.objects.filter(time=time, day=day, division=division,
                                                         is_practical=True,
                                                         batch=batch)
                    if timetable:
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

                        timetable.save()

        # to_json(request)
        to_json()
        return HttpResponseRedirect('/timetable/enter/')
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

        answer[year][branch][division][day][time] = {
            'faculty': faculty,
            'room': room,
            'subject': subject
        }

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

        answer[year][branch][division][day][time] = {
            'faculty': faculty,
            'room': room,
            'subject': subject
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


def get_excel(request):
    if request.method == 'GET':
        return render(request, 'get_excel.html')
    else:
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        if request.POST.get('button_type') == 'Generate':
            year = request.POST.get('year')
            branch = request.POST.get('branch')
            division = request.POST.get('division')

            branch_obj = Branch.objects.get(branch=branch)
            college_year = CollegeYear.objects.filter(year=year).first()
            timetable = Timetable.objects.filter(branch_subject__year=college_year, branch_subject__branch=branch_obj,
                                                 division__division=division).order_by('time__starting_time')

            workbook = xlsxwriter.Workbook(
                'media/documents/Timetable_' + year + "_" + branch + "_" + division + '.xlsx')
            worksheet = workbook.add_worksheet()

            worksheet.set_column(0, 9, 16)

            offset_x = 0
            offset_y = 0

            times = timetable.values_list('time__starting_time', flat=True).order_by('time__starting_time').distinct()
            time_index = {}
            time_row = 1
            for time in times:
                time_index[time] = time_row
                time_row += 1
            row = 0
            col = 0
            for tt in timetable:
                curr_col = days.index(tt.day) + 1
                curr_row = time_index.get(tt.time.starting_time)
                worksheet.write(row, curr_col, tt.day)

                worksheet.write(curr_row, col, tt.time.__str__())

                worksheet.write(curr_row, curr_col,
                                tt.faculty.initials + " " + tt.branch_subject.subject.short_form + " " +
                                tt.room.room_number)
            workbook.close()


        elif request.POST.get('button_type') == 'UG':
            year = request.POST.get('year')
            branch = request.POST.get('branch')
            branch_obj = Branch.objects.get(branch=branch)
            college_year = CollegeYear.objects.filter(year=year).first()
            timetable = Timetable.objects.filter(branch_subject__year=college_year,
                                                 branch_subject__branch=branch_obj).order_by('time__starting_time')

            workbook = xlsxwriter.Workbook(
                'media/documents/Timetable_' + year + "_" + branch + '.xlsx')
            worksheet = workbook.add_worksheet()

            offset_x = 0
            offset_y = 0

            times = timetable.values_list('time__starting_time', flat=True).order_by('time__starting_time').distinct()
            time_index = {}
            time_row = 1
            for time in times:
                time_index[time] = time_row
                time_row += 1

            divs = timetable.values_list('division__division', flat=True).distinct().order_by('division__division')
            total_divs = divs.__len__()
            div_index = {}
            div_col = 0

            for div in divs:
                div_index[div] = div_col
                div_col += 1

            row = 0
            col = 0
            for tt in timetable:
                curr_col = days.index(tt.day)
                curr_row = time_index.get(tt.time.starting_time) + 1

                worksheet.set_column(firstcol=0, lastcol=30, width=15)

                worksheet.write(row, curr_col * total_divs + 1, tt.day)

                worksheet.write(curr_row + 1, col, tt.time.__str__())

                worksheet.write(row + 1, curr_col * total_divs + div_index.get(tt.division.division) + 1,
                                tt.division.division)
                worksheet.write(curr_row, curr_col * total_divs + div_index.get(tt.division.division) + 1,
                                tt.faculty.initials + " " + tt.branch_subject.subject.short_form + " " +
                                tt.room.room_number)

            workbook.close()
        return HttpResponse('Done')
