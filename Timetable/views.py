import json
from collections import defaultdict

import firebase_admin
from django.http.response import HttpResponseRedirect
from firebase_admin import credentials, db
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User

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
    room = [i.room_number for i in Room.objects.filter(branch=branch_obj, lab=False)]
    subjects_obj = BranchSubject.objects.filter(branch=branch_obj)
    subjects = []
    faculty = []
    divisions_js = ""
    for i in divisions:
        divisions_js += i

    timetables = Timetable.objects.filter(is_practical=False)
    timetable_prac = Timetable.objects.filter(is_practical=True)

    context = {
        'branch': branch,
        'times': times,
        'year': years,
        'days': days,
        'division': divisions,
        'number_of_division': range(len(divisions)),
        'room': room,
        'subjects': subjects,
        'faculty': faculty,
        'divisions_js': divisions_js,
        'timetables': timetables,
        'timetable_prac': timetable_prac
    }
    return render(request, 'fill_timetable.html', context)


def get_faculty(request):
    if request.is_ajax():
        subject = request.POST.get('subject')
        division = request.POST.get('division')
        year = request.POST.get('year')
        subject_obj = Subject.objects.get(short_form=subject)
        # faculty_subject = FacultySubject.objects.filter(subject=subject_obj).filter(division=division)
        # faculty = []
        # for each in faculty_subject:
        #     faculty.append(each.faculty.first_name)
        branch_obj = Branch.objects.get(branch='Computer')
        year_obj = CollegeYear.objects.get(year=year)
        college_obj_general = CollegeExtraDetail.objects.filter(Q(branch=branch_obj),
                                                                Q(year=year_obj))
        college_obj = college_obj_general.get(division=division)
        # college_obj = CollegeExtraDetail.objects.filter(branch=branch_obj).filter(year=year_obj).filter(
        #     division=division)
        # Right now have not handled for multiple faculty
        faculty_subject = FacultySubject.objects.filter(Q(division=college_obj),
                                                        Q(subject=subject_obj))
        test = FacultySubject.objects.filter(Q(faculty=faculty_subject[0].faculty),
                                             Q(subject=subject_obj))
        disable_division = [i.division.division for i in test]
        disable_division.remove(division)
        faculty = []

        for each in faculty_subject:
            faculty.append((each.faculty.initials + '-' + each.faculty.faculty_code))
        is_practical = subject_obj.is_practical

        data = {'faculty': faculty, 'divisions': disable_division, 'practical': is_practical}
        if is_practical is True:
            data['batches'] = list(college_obj.batch_set.values_list('batch_name', flat=True))
        return HttpResponse(json.dumps(data))


def save_timetable(request):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    if request.method == 'POST':



        selected_list = request.POST

        for key in selected_list:
            if not (str(key).__contains__("_room_choices") or str(key).__contains__("_faculty") or str(
                    key).__contains__('csrfmiddlewaretoken')):
                starting_time_str = str(key).split("room_")[1].split("-")[0].split(':')
                starting_time = int(starting_time_str[0]) * 100 + int(starting_time_str[1])
                ending_time_str = str(key).split("room_")[1].split("-")[1].split('_')[0].split(':')
                ending_time = int(ending_time_str[0]) * 100 + int(ending_time_str[1])
                time = Time.objects.get(starting_time=starting_time,
                                        ending_time=ending_time)
                # branch filter krni hai
                branch_obj = Branch.objects.get(branch='Computer')
                branch_subject = BranchSubject.objects.get(
                    subject=Subject.objects.get(short_form=selected_list.get(key)))
                division = str(key).split('_')[3]
                day = days[int(str(key).split('_')[4]) - 2]

                faculty = Faculty.objects.get(faculty_code=selected_list.get(key + '_faculty'))

                room = Room.objects.get(room_number=selected_list.get(key + '_room_choices'))

                # timetable_exists = Timetable.objects.filter(room=room, faculty=faculty, division=division, branch_subject=branch_subject,
                #                       time=time, day=day)
                # shift ka bacha hai. ho jana chahiye
                division_object = CollegeExtraDetail.objects.get(branch=branch_obj, year=branch_subject.year,
                                                                 division=division)
                timetable_exists = Timetable.objects.filter(division=division_object,
                                                            branch_subject=branch_subject, time=time, day=day).first()
                timetable_obj = []
                if (timetable_exists):
                    print("Already exists")
                    timetable_exists.room = room
                    timetable_exists.faculty = faculty
                    timetable_exists.is_practical = True
                    timetable_exists.save()

                else:

                    timetable_exists = Timetable(room=room, faculty=faculty, division=division_object,
                                                 branch_subject=branch_subject,
                                                 time=time, day=day)
                    timetable_obj.append(timetable_exists)

                Timetable.objects.bulk_create(timetable_obj)


                # if str(key).__contains__("_room"):
                #     room = Room.objects.get(room_number=selected_list.get(key))
                #
                # elif str(key).__contains__("_faculty"):
                #     faculty = Faculty.objects.get(faculty_code=selected_list.get(key))
                #
                #     division = str(key).split('_')[3]
                #     day = days[int(str(key).split('_')[4]) - 2]
                # elif str(key).__contains__("id_room_"):
                #     branch_subject = BranchSubject.objects.filter(
                #         subject=Subject.objects.filter(short_form=selected_list.get(key)))
                #     starting_time_str = str(key).split("room_")[1].split("-")[0].split(':')
                #     starting_time = int(starting_time_str[0]) * 100 + int(starting_time_str[1])
                #     ending_time_str = str(key).split("room_")[1].split("-")[1].split('_')[0].split(':')
                #     ending_time = int(ending_time_str[0]) * 100 + int(ending_time_str[1])
                #     time = Time.objects.filter(starting_time=starting_time,
                #                                ending_time=ending_time)

                #
                #
                # # need to be changed with subject code
                # #
        to_json(request)
        return HttpResponse('Saved')
    else:
        return HttpResponse('Not Post')


def to_json(request):
    full_timetable = Timetable.objects.all()
    answer = {}
    time_json = {}
    day_json = {}
    division_json = {}
    branch_json = {}
    year_json = {}
    output = ""
    # key = {}
    # key['test'] = 'inner'
    # key['test']['inner'] = 'hello'

    for year in full_timetable.values_list('branch_subject__year__year', flat=True).distinct():
        branch_filtered = full_timetable.filter(
            branch_subject__in=BranchSubject.objects.filter(year=CollegeYear.objects.get(year=year)))
        year_json = {}
        for branch in set(branch_filtered.values_list(
                'branch_subject__branch__branch', flat=True)):
            division_filtered = branch_filtered.filter(
                branch_subject__in=BranchSubject.objects.filter(branch=Branch.objects.get(
                    branch=branch)))
            branch_json = {}
            for division in division_filtered.values_list('division__division', flat=True):
                day_filtered = division_filtered.filter(division__division=division)
                division_json = {}
                for day in set(day_filtered.values_list('day', flat=True)):
                    time_filtered = day_filtered.filter(day=day)
                    day_json = {}
                    for table in time_filtered.only('time'):
                        time_json['faculty'] = copy.deepcopy(table.faculty.initials)
                        time_json['room'] = copy.deepcopy(table.room.room_number)
                        time_json['subject'] = copy.deepcopy(table.branch_subject.subject.short_form)
                        day_json[str(table.time.format_for_json())] = copy.deepcopy(time_json)
                    division_json[day] = copy.deepcopy(day_json)
                branch_json[division] = copy.deepcopy(division_json)
                year_json[branch] = copy.deepcopy(branch_json)
                answer[year] = year_json


                # for each in full_timetable:
                #     # answer[each.branch_subject.year.year] =
                #     time['faculty'] = each.faculty.user.first_name
                #     time['room'] = each.room.room_number
                #     time['subject'] = each.branch_subject.subject.name
                #     if str(each.time.starting_time) + '-' + str(each.time.ending_time) in day:
                #         day[str(each.time.starting_time) + '-' + str(each.time.ending_time)].append(time)
                #     else:
                #         day[str(each.time.starting_time) + '-' + str(each.time.ending_timgie)] = time
                #         # if each.day in division:
                #         #     division[str(each.day)].append(day)
                #         # else:
                #         division[each.day] = day
                #         output += str(day)
    write_to_firebase(answer, 'Student')

    full_timetable = Timetable.objects.all()
    # answer = {}
    time_json = {}
    day_json = {}
    division_json = {}
    branch_json = {}
    year_json = {}
    output = ""
    # key = {}
    # key['test'] = 'inner'
    # key['test']['inner'] = 'hello'
    answer2 = {}
    faculty_json = {}
    temp = {}
    for faculty in full_timetable.values_list('faculty__initials', flat=True).distinct():
        temp_full = full_timetable.filter(faculty=Faculty.objects.get(initials=faculty))
        for day in set(temp_full.values_list('day', flat=True)):
            time_filtered = temp_full.filter(day=day)
            day_json = {}
            for table in time_filtered.only('time'):
                time_json['room'] = copy.deepcopy(table.room.room_number)
                time_json['subject'] = copy.deepcopy(table.branch_subject.subject.short_form)
                time_json['branch'] = copy.deepcopy(table.branch_subject.branch.branch)
                time_json['division'] = copy.deepcopy(table.division.division)
                time_json['year'] = copy.deepcopy(table.branch_subject.year.year)
                day_json[str(table.time.format_for_json())] = copy.deepcopy(time_json)

            faculty_json[day] = copy.deepcopy(day_json)
            temp[faculty] = copy.deepcopy(faculty_json)
    write_to_firebase(temp, 'Faculty')
    return HttpResponse(str(answer))


def get_all_faculty_subject(request):
    branch = request.POST.get('branch')
    branch_obj = Branch.objects.get(branch=branch)
    all_subjects = set(BranchSubject.objects.filter(branch=branch_obj).values_list('subject', flat=True))
    all_subjects_obj = [Subject.objects.get(code=i) for i in all_subjects]
    all_faculty = FacultySubject.objects.filter(subject__in=all_subjects_obj).values_list('faculty__initials',
                                                                                          flat=True).distinct()
    all_faculty_js = ""
    for i in all_faculty:
        all_faculty_js += i
        all_faculty_js += ','
    return HttpResponse(all_faculty_js)


def get_timetable(request):
    tt_instance_practical = []
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    year = request.POST.get('year')

    branch = request.POST.get('branch')
    all_year = list(CollegeYear.objects.all())
    clg_year = CollegeYear.objects.get(year=year)
    all_year.remove(clg_year)
    branch_obj = Branch.objects.get(branch=branch)
    branch_subject = BranchSubject.objects.filter(year=clg_year, branch=branch_obj,
                                                  subject__is_practical=False).distinct()
    remove_subjects = BranchSubject.objects.filter(year__in=all_year, branch=branch_obj).distinct()
    timetable_assigned = {}

    timetable_assigned_blocked = {}
    actual_assigned = {'faculty': []}

    actual_assigned_blocked = {'faculty': []}
    tt_instance = []
    for i in branch_subject:
        for faculty in list(FacultySubject.objects.filter(subject=i.subject).values_list('faculty__initials',
                                                                                         flat=True).distinct()):
            actual_assigned['faculty'].append(faculty)

        for j in list(Timetable.objects.filter(branch_subject=i).distinct()):
            tt_instance.append(
                j.room.room_number + "**" + j.branch_subject.subject.short_form + "**" + j.faculty.faculty_code + "**" + j.faculty.initials + "**" +
                "id_room_" + j.time.__str__() + "_" + j.division.division + "_" + str(days.index(j.day) + 2))
            if j.faculty.initials not in timetable_assigned:
                timetable_assigned[j.faculty.initials] = []
            timetable_assigned[j.faculty.initials].append(
                "id_room_" + j.time.__str__() + "_" + j.division.division + "_" + str(days.index(j.day) + 2))

    branch_subject = BranchSubject.objects.filter(year=clg_year, branch=branch_obj,
                                                  subject__is_practical=True).distinct()
    for i in branch_subject:
        for faculty in list(FacultySubject.objects.filter(subject=i.subject).values_list('faculty__initials',
                                                                                         flat=True).distinct()):
            actual_assigned['faculty'].append(faculty)

        for j in list(Timetable.objects.filter(branch_subject=i).distinct()):
            tt_instance_practical.append(
                "id_room_" + j.time.__str__() + "_" + j.division.division + "_" + str(days.index(j.day) + 2))
            if j.faculty.initials not in timetable_assigned:
                timetable_assigned[j.faculty.initials] = []
            timetable_assigned[j.faculty.initials].append(
                "id_room_" + j.time.__str__() + "_" + j.division.division + "_" + str(days.index(j.day) + 2))

        tt_instance_practical = list(set(tt_instance_practical))


            # timetable_assigned[j.faculty.initials] ="id_room_" + j.time.__str__() + "_" + j.division.division + "_" + str(days.index(j.day) + 2)

    for i in remove_subjects:
        for faculty in list(FacultySubject.objects.filter(subject=i.subject).values_list('faculty__initials',
                                                                                         flat=True).distinct()):
            actual_assigned_blocked['faculty'].append(faculty)

        for j in list(Timetable.objects.filter(branch_subject=i).distinct()):
            tt_instance.append(
                "id_room_" + j.time.__str__() + "_" + j.division.division + "_" + str(days.index(j.day) + 2))
            if j.faculty.initials not in timetable_assigned:
                timetable_assigned_blocked[j.faculty.initials] = []
            timetable_assigned_blocked[j.faculty.initials].append(
                "id_room_" + j.time.__str__() + "_" + j.division + "_" + str(days.index(j.day) + 2))

            # timetable_assigned[j.faculty.initials] ="id_room_" + j.time.__str__() + "_" + j.division + "_" + str(days.index(j.day) + 2)


    # timetable = Timetable.objects.filter(branch_subject__in=branch_subject)
    #
    # subjects = timetable.values_list('subject')

    subjects = BranchSubject.objects.filter(year=CollegeYear.objects.get(year=year), branch=branch_obj)
    subjects_theory = list(subjects.filter(subject__is_practical=False).values_list(
        'subject__short_form', flat=True))
    subjects_practical = list(subjects.filter(subject__is_practical=True).values_list(
        'subject__short_form', flat=True))
    answer = {
        'timetable_assigned': timetable_assigned,
        'actual_assigned': actual_assigned,
        'timetable_assigned_blocked': timetable_assigned_blocked,
        'actual_assigned_blocked': actual_assigned_blocked,
        'subjects_theory': subjects_theory,
        'subjects_practical': subjects_practical,
        'tt_instance': str(tt_instance),
        'tt_instance_practical': tt_instance_practical
    }
    return JsonResponse(answer)


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
            # print(divs, total_divs, "total===============")

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


def get_instance(request):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    year = request.POST.get('year')
    # print(year, "get_timetable")

    branch = request.POST.get('branch')
    clg_year = CollegeYear.objects.get(year=year)
    branch_obj = Branch.objects.get(branch=branch)
    branch_subject = BranchSubject.objects.filter(year=clg_year, branch=branch_obj).distinct()
    # print(branch_subject)
    tt_instance = []
    for i in branch_subject:
        for j in list(Timetable.objects.filter(branch_subject=i).distinct().order_by('day', 'time__starting_time',
                                                                                     'division__division')):
            tt_instance.append(
                j.room.room_number + "**" + j.branch_subject.subject.short_form + "**" + j.faculty.faculty_code + "**" + j.faculty.initials + "**" +
                "id_room_" + j.time.__str__() + "_" + j.division + "_" + str(days.index(j.day) + 2))

    # print("instance tt", tt_instance)

    return HttpResponse(str(tt_instance))


def get_practical_info(request):
    day = request.POST.get('prac_day')
    day=str(day)
    start_time = request.POST.get('prac_starting_time')
    branch = request.POST.get('branch')
    year = request.POST.get('year')
    division = request.POST.get('division')
    division_obj = CollegeExtraDetail.objects.get(division=division)
    data = {}
    batches = list(
        Batch.objects.filter(division=division_obj).values_list('batch_name',
                                                                                                     flat=True))
    data['batches'] = batches
    branch_obj = Branch.objects.get(branch=branch)
    subjects = BranchSubject.objects.filter(year=CollegeYear.objects.get(year=year), branch=branch_obj)
    subjects_practical = list(subjects.filter(subject__is_practical=True).values_list(
        'subject__short_form', flat=True))
    rooms = list(Room.objects.filter(branch=branch_obj, lab=True).values_list('room_number', flat=True))
    data['subjects'] = subjects_practical
    data['rooms'] = rooms
    if day!= 'false':
        time_obj = Time.objects.get(starting_time=start_time)
        temp = {}
        for i in Timetable.objects.filter(time=time_obj,day=day,division= division_obj,is_practical=True):
            temp[i.batch.batch_name] = {
                'faculty':i.faculty.initials,
                'subject':i.branch_subject.subject.short_form,
                'room': i.room.room_number
            }
        data['selected']=temp
    return HttpResponse(json.dumps(data))


def get_practical_faculty(request):
    faculty = []
    branch = request.POST.get('branch')
    year = request.POST.get('year')
    subject = request.POST.get('subject')
    division = request.POST.get('division')
    year_obj = CollegeYear.objects.get(year=year)
    subject_obj = Subject.objects.get(short_form=subject)
    branch_obj = Branch.objects.get(branch=branch)
    division_obj = CollegeExtraDetail.objects.get(division=division, year=year_obj, branch=branch_obj)
    faculty_subject = FacultySubject.objects.filter(Q(division=division_obj),
                                                    Q(subject=subject_obj))
    for each in faculty_subject:
        faculty.append((each.faculty.initials + '*.*' + each.faculty.faculty_code))

    data = {}
    data['faculty'] = faculty
    return HttpResponse(json.dumps(data))


def save_practical(request):
    # print(request.POST)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    if request.method == 'POST':



        selected_list = request.POST

        division = ''

        # print(selected_list,'=========================================')
        for key in selected_list:
            if str(key).__contains__('id_room_'):


                starting_time_str = str(key).split("room_")[1].split("-")[0].split(':')
                starting_time = int(starting_time_str[0]) * 100 + int(starting_time_str[1])
                ending_time_str = str(key).split("room_")[1].split("-")[1].split('_')[0].split(':')
                ending_time = int(ending_time_str[0]) * 100 + int(ending_time_str[1])
                # print(starting_time, ending_time)
                time = Time.objects.get(starting_time=starting_time,
                                        ending_time=ending_time)

                division = str(key).split('_')[3]
                # print(division)
                day = days[int(str(key).split('_')[4]) - 2]
                # print(day)
                break
        for key in selected_list:
            # branch filter krni hai
            if str(key).__contains__("modal_room"):
                key_arr = str(key).split('_')

                branch_obj = Branch.objects.get(branch='Computer')
                branch_subject = BranchSubject.objects.get(
                    subject=Subject.objects.get(short_form=selected_list.get(key_arr[0] + '_subject_' + key_arr[2])))

                faculty = Faculty.objects.get(faculty_code=selected_list.get(key_arr[0] + '_faculty_' + key_arr[2]))

                room = Room.objects.get(room_number=selected_list.get(key_arr[0] + '_room_' + key_arr[2]))

                # timetable_exists = Timetable.objects.filter(room=room, faculty=faculty, division=division, branch_subject=branch_subject,
                #                       time=time, day=day)
                # shift ka bacha hai. ho jana chahiye

                division_object = CollegeExtraDetail.objects.get(branch=branch_obj, year=branch_subject.year,
                                                                 division=division)
                batch = Batch.objects.get(batch_name=key_arr[2], division=division_object)
                timetable_exists = Timetable.objects.filter(division=division_object,
                                                            branch_subject=branch_subject, time=time, day=day,
                                                            batch=batch).first()
                timetable_obj = []
                if (timetable_exists):
                    # print("Already exists")
                    timetable_exists.room = room
                    timetable_exists.faculty = faculty
                    timetable_exists.is_practical = True
                    timetable_exists.save()

                else:

                    timetable_exists = Timetable(room=room, faculty=faculty, division=division_object,
                                                 branch_subject=branch_subject,
                                                 time=time, day=day, batch=batch, is_practical=True)
                    timetable_obj.append(timetable_exists)

                Timetable.objects.bulk_create(timetable_obj)

        return HttpResponse('Saved')
    else:
        return HttpResponse('Not Post')
