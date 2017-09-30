import json
from collections import defaultdict

import firebase_admin
from firebase_admin import credentials, db
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

from General.models import CollegeExtraDetail, BranchSubject, FacultySubject, CollegeYear
# from .forms import TimetableForm
from Registration.models import Branch, Subject, Faculty
from .models import Time, Room, Timetable
from Registration.models import Branch, Subject
from .models import Time, Room, Timetable
import copy
from Sync.function import write_to_firebase


# Create your views here.

def fill_timetable(request):
    times = []
    years = []
    # branch = Branch.objects.all()
    branch_obj = Branch.objects.get(branch='Computer')
    branch = branch_obj.branch
    for i in Time.objects.all():
        times.append(i.__str__())

    for i in CollegeYear.objects.all().order_by('year').values_list('year', flat=True).distinct():
        years.append(i)

    divisions = CollegeExtraDetail.objects.filter(branch=branch_obj).order_by('division').values_list('division',
                                                                                                      flat=True).distinct()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    # form = TimetableForm()
    # branch = Branch.objects.all().values_list('branch', flat=True)
    room = [i.room_number for i in Room.objects.filter(branch=branch_obj)]
    print('Timetable-fill_timetable-rooms', room)
    print(branch)
    subjects_obj = BranchSubject.objects.filter(branch=branch_obj)
    subjects = []
    faculty = []
    print("Timetable:fill_timetable-divisions", divisions)
    divisions_js = ""
    for i in divisions:
        divisions_js += i
    print(divisions_js)

    timetables = Timetable.objects.all()
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
        'timetables': timetables
    }
    return render(request, 'fill_timetable.html', context)


def get_faculty(request):
    if request.is_ajax():
        subject = request.POST.get('subject')
        division = request.POST.get('division')
        year = request.POST.get('year')
        print("Subject:", subject)
        print('division', division)
        subject_obj = Subject.objects.get(short_form=subject)
        # faculty_subject = FacultySubject.objects.filter(subject=subject_obj).filter(division=division)
        # faculty = []
        # for each in faculty_subject:
        #     faculty.append(each.faculty.first_name)
        branch_obj = Branch.objects.get(branch='Computer')
        year_obj = CollegeYear.objects.get(year=year)
        college_obj_general = CollegeExtraDetail.objects.filter(Q(branch=branch_obj),
                                                                Q(year=year_obj))
        college_obj = college_obj_general.filter(division=division)
        # college_obj = CollegeExtraDetail.objects.filter(branch=branch_obj).filter(year=year_obj).filter(
        #     division=division)
        print("ajax college_object", college_obj)
        # Right now have not handled for multiple faculty
        faculty_subject = FacultySubject.objects.filter(Q(division=college_obj),
                                                        Q(subject=subject_obj))
        test = FacultySubject.objects.filter(Q(faculty=faculty_subject[0].faculty),
                                             Q(subject=subject_obj))
        disable_division = [i.division.division for i in test]
        disable_division.remove(division)
        print("Testing...", disable_division)
        faculty = []

        for each in faculty_subject:
            faculty.append((each.faculty.user.first_name + '-' + each.faculty.faculty_code))
            print("each_faculty", each.faculty.user)
        print('Timetable-get_faculty:faculty', faculty)

        data = {'faculty': faculty, 'divisions': disable_division}
        return HttpResponse(json.dumps(data))


def get_subject(request):
    year = request.POST.get('year')
    subjects = BranchSubject.objects.filter(year=CollegeYear.objects.get(year=year))
    subject_list = [i.subject.short_form for i in subjects]
    subject_string = ",".join(subject_list)
    return HttpResponse(subject_string)


def save_timetable(request):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    if request.method == 'POST':
        # print(request.POST.get)
        selected_list = request.POST

        print(selected_list)
        for key in selected_list:
            if not (str(key).__contains__("_room_choices") or str(key).__contains__("_faculty") or str(
                    key).__contains__('csrfmiddlewaretoken')):
                print(key)
                starting_time_str = str(key).split("room_")[1].split("-")[0].split(':')
                starting_time = int(starting_time_str[0]) * 100 + int(starting_time_str[1])
                ending_time_str = str(key).split("room_")[1].split("-")[1].split('_')[0].split(':')
                ending_time = int(ending_time_str[0]) * 100 + int(ending_time_str[1])
                print(starting_time, ending_time)
                time = Time.objects.get(starting_time=starting_time,
                                        ending_time=ending_time)
                # branch filter krni hai
                branch_subject = BranchSubject.objects.get(
                    subject=Subject.objects.get(short_form=selected_list.get(key)))
                division = str(key).split('_')[3]
                print(division)
                day = days[int(str(key).split('_')[4]) - 2]
                print(day)

                faculty = Faculty.objects.get(faculty_code=selected_list.get(key + '_faculty'))

                room = Room.objects.get(room_number=selected_list.get(key + '_room_choices'))

                # timetable_exists = Timetable.objects.filter(room=room, faculty=faculty, division=division, branch_subject=branch_subject,
                #                       time=time, day=day)
                timetable_exists = Timetable.objects.filter(division=division,
                                                            branch_subject=branch_subject, time=time, day=day).first()
                if (timetable_exists):
                    print("Already exists")
                    timetable_exists[0].room = room
                    timetable_exists[0].faculty = faculty
                    timetable_exists[0].save()

                else:
                    print("Not exists")

                    timetable_exists = Timetable(room=room, faculty=faculty, division=division,
                                                 branch_subject=branch_subject,
                                                 time=time, day=day)
                    timetable_exists.save()



                    # if str(key).__contains__("_room"):
                    #     room = Room.objects.get(room_number=selected_list.get(key))
                    #
                    # elif str(key).__contains__("_faculty"):
                    #     faculty = Faculty.objects.get(faculty_code=selected_list.get(key))
                    #
                    #     division = str(key).split('_')[3]
                    #     print(division)
                    #     day = days[int(str(key).split('_')[4]) - 2]
                    #     print(day)
                    # elif str(key).__contains__("id_room_"):
                    #     branch_subject = BranchSubject.objects.filter(
                    #         subject=Subject.objects.filter(short_form=selected_list.get(key)))
                    #     starting_time_str = str(key).split("room_")[1].split("-")[0].split(':')
                    #     starting_time = int(starting_time_str[0]) * 100 + int(starting_time_str[1])
                    #     ending_time_str = str(key).split("room_")[1].split("-")[1].split('_')[0].split(':')
                    #     ending_time = int(ending_time_str[0]) * 100 + int(ending_time_str[1])
                    #     # print(starting_time, ending_time)
                    #     time = Time.objects.filter(starting_time=starting_time,
                    #                                ending_time=ending_time)

                    # print(time, "timeeeee")
                    #
                    # print(faculty, "facultyyyyyyyyy")
                    #
                    # # need to be changed with subject code
                    # #
                    # print(branch_subject, "subject!!!!!!!!")
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
    # print(key)



    for year in full_timetable.values_list('branch_subject__year__year', flat=True).distinct():
        # print("year", year)
        branch_filtered = full_timetable.filter(
            branch_subject__in=BranchSubject.objects.filter(year=CollegeYear.objects.get(year=year)))
        year_json = {}
        for branch in set(branch_filtered.values_list(
                'branch_subject__branch__branch', flat=True)):
            # print('branch', branch)
            division_filtered = branch_filtered.filter(
                branch_subject__in=BranchSubject.objects.filter(branch=Branch.objects.get(
                    branch=branch)))
            branch_json = {}
            for division in set(division_filtered.values_list('division', flat=True)):
                # print('division', division)
                day_filtered = division_filtered.filter(division=division)
                division_json = {}
                for day in set(day_filtered.values_list('day', flat=True)):
                    # print('day', day)
                    time_filtered = day_filtered.filter(day=day)
                    day_json = {}
                    for table in time_filtered.only('time'):
                        # print('time', table.time)
                        time_json['faculty'] = copy.deepcopy(table.faculty.initials)
                        time_json['room'] = copy.deepcopy(table.room.room_number)
                        time_json['subject'] = copy.deepcopy(table.branch_subject.subject.short_form)
                        day_json[str(table.time.format_for_json())] = copy.deepcopy(time_json)
                    division_json[day] = copy.deepcopy(day_json)
                branch_json[division] = copy.deepcopy(division_json)
                year_json[branch] = copy.deepcopy(branch_json)
                answer[year] = year_json


                # for each in full_timetable:
                #     # print(each)
                #     # answer[each.branch_subject.year.year] =
                #     time['faculty'] = each.faculty.user.first_name
                #     time['room'] = each.room.room_number
                #     time['subject'] = each.branch_subject.subject.name
                #     if str(each.time.starting_time) + '-' + str(each.time.ending_time) in day:
                #         day[str(each.time.starting_time) + '-' + str(each.time.ending_time)].append(time)
                #     else:
                #         day[str(each.time.starting_time) + '-' + str(each.time.ending_time)] = time
                #         # # print(time)
                #         print(each.day)
                #         # if each.day in division:
                #         #     division[str(each.day)].append(day)
                #         # else:
                #         division[each.day] = day
                #         print(day)
                #         output += str(day)
    write_to_firebase(answer)
    return HttpResponse(str(answer))


def get_all_faculty_subject(request):
    # print(request.POST)
    branch = request.POST.get('branch')
    print(branch)
    branch_obj = Branch.objects.get(branch=branch)
    all_subjects = set(BranchSubject.objects.filter(branch=branch_obj).values_list('subject', flat=True))
    all_subjects_obj = [Subject.objects.get(code=i) for i in all_subjects]
    all_faculty = FacultySubject.objects.filter(subject__in=all_subjects_obj).values_list('faculty__initials',
                                                                                          flat=True).distinct()
    print('here')
    print(all_faculty)
    all_faculty_js = ""
    for i in all_faculty:
        all_faculty_js += i
        all_faculty_js += ','
    return HttpResponse(all_faculty_js)


def get_timetable(request):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    year = request.POST.get('year')
    print(year, "get_timetable")

    branch = request.POST.get('branch')
    clg_year = CollegeYear.objects.get(year=year)
    branch_obj = Branch.objects.get(branch=branch)
    branch_subject = BranchSubject.objects.filter(year=clg_year, branch=branch_obj).distinct()
    print(branch_subject)
    timetable_assigned = {}
    actual_assigned = {}
    actual_assigned['faculty'] = []
    for i in branch_subject:
        for faculty in list(FacultySubject.objects.filter(subject=i.subject).values_list('faculty__initials',
                                                                                         flat=True).distinct()):
            actual_assigned['faculty'].append(faculty)
            
        for j in list(Timetable.objects.filter(branch_subject=i).distinct()):
            if j.faculty.initials not in timetable_assigned:
                timetable_assigned[j.faculty.initials] = []
                # timetable_assigned[j.faculty.initials].append("id_room_" + j.time.__str__() + "_" + j.division + "_" + str(
                #     days.index(j.day) + 2))
            timetable_assigned[j.faculty.initials].append(
                "id_room_" + j.time.__str__() + "_" + j.division + "_" + str(days.index(j.day) + 2))

            # timetable_assigned[j.faculty.initials] ="id_room_" + j.time.__str__() + "_" + j.division + "_" + str(days.index(j.day) + 2)

            print(j)

        # timetable = Timetable.objects.filter(branch_subject__in=branch_subject)
        #
        # subjects = timetable.values_list('subject')

        # print(timetable, "Timetble!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    answer = {
            'timetable_assigned': timetable_assigned,
            'actual_assigned': actual_assigned
        }
    return HttpResponse(json.dumps(answer), 'application/javascript')
