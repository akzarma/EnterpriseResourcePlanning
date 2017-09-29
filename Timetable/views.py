import json

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from General.models import CollegeExtraDetail, BranchSubject, FacultySubject, CollegeYear
# from .forms import TimetableForm
from Registration.models import Branch, Subject
from .models import Time, Room, Timetable
import copy


# Create your views here.

def fill_timetable(request):
    times = []
    years = []
    # branch = Branch.objects.all()
    branch_obj = Branch.objects.get(branch='Computer')
    branch = branch_obj.branch
    for i in Time.objects.all():
        times.append(i)

    for i in CollegeYear.objects.all().values_list('year', flat=True):
        years.append(i)

    divisions = list(CollegeExtraDetail.objects.filter(branch=branch_obj).values_list('division', flat=True))
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    # form = TimetableForm()
    # branch = Branch.objects.all().values_list('branch', flat=True)
    room = Room.objects.filter(branch=branch_obj).values_list('room_number')
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
    }
    return render(request, 'fill_timetable.html', context)


def get_faculty(request):
    if request.is_ajax():
        subject = request.POST.get('subject')
        division = request.POST.get('division')
        year = request.POST.get('year')
        print("Subject:", subject)
        print('division', division)
        subject_obj = Subject.objects.get(name=subject)
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
            faculty.append(each.faculty.user.first_name)
            print("each_faculty", each.faculty.user)
        print('Timetable-get_faculty:faculty', faculty)

        data = {'faculty': faculty, 'divisions': disable_division}
        return HttpResponse(json.dumps(data))


def convert_json(request):
    lecture_detail = Timetable.objects.all()
    a = []
    for k in BranchSubject.objects.filter(year=CollegeYear.objects.get(year='TE')):
        a.append(k)
    print(Timetable.objects.filter(BranchSubject.objects.filter(year=CollegeYear.objects.get(year='TE'))),
          "jihyugytvytvytvytvytvytv")

    sent_json = [{
        j.branch_subject.year.year: {
            k: {
                l: {
                    (str(j.time.starting_time) + '-' + str(j.time.ending_time)): {
                        'faculty': str(j.faculty.user.first_name),
                        'room': str(j.room.room_number),
                        'subject': str(j.branch_subject.subject.short_form)
                    }
                }
                for l in Timetable.objects.filter(division=k.division)
            }
            for k in Timetable.objects.filter(
            branch_subject=BranchSubject.objects.filter(year=CollegeYear.objects.get(year=j.branch_subject.year.year)))

        } for j in lecture_detail
    }]

    # for i in timetable:
    #     sent_json.append({
    #         i.branch_subject.year.year: {
    #             i.branch_subject.branch.branch: {
    #                 i.division: {
    #                     i.day: {
    #                         (str(i.time.starting_time) + '-' + str(i.time.ending_time)): {
    #                             'faculty': str(i.faculty.user.first_name),
    #                             'room': str(i.room.room_number),
    #                             'subject': str(i.branch_subject.subject.short_form)
    #                         }
    #                     }
    #                 }
    #             }
    #         }
    #     })

    return HttpResponse(a)

#
# def to_json(request):
#     timetable = Timetable.objects.all()
#     print("Timetable-to_json:full_timetable: ", timetable)
#     year_json = {}
#
#     for i in range(timetable.__len__()):
#         year = timetable[i].branch_subject.year.year
#         # year_json[year] = year
#         time = str(timetable[i].time.starting_time) + '-' + str(timetable[i].time.ending_time)
#         faculty = timetable[i].faculty.faculty_code
#         room = timetable[i].room.room_number
#         subject = timetable[i].branch_subject.subject.name
#         day = timetable[i].day
#         division = timetable[i].division
#         branch = timetable[i].branch_subject.branch.branch
#
#         # Innermost JSON
#         lecture_json = {}
#         lecture_json['faculty'] = faculty
#         lecture_json['room'] = room
#         lecture_json['subject'] = subject
#
#         # print(subject)
#         # subject_json['subject'] = subject
#         # print(subject_json)
#
#         # Last but Innermost JSON
#         time_json = {}
#         time_json[time] = (lecture_json)
#         print("time_json", time_json)
#
#         # Last but last but innermost JSON
#         day_json = {}
#         day_json[day] = time_json
#         print("day_json", day_json)
#
#         # Third outermost JSON
#         division_json = {division: day_json}
#         # division_json = json.dumps(division_json)
#
#         # Second outermost JSON
#         branch_json = {branch: division_json}
#
#         # Outermost JSON
#         # year_json = {}
#         year_json[year] = branch_json
#         # print(year_json)
#
#         # Full JSON
#         # full[year] = year_json
#
#     # final = json.dumps(year_json).__str__();
#     return HttpResponse(year_json.__str__())


def to_json(request):
    timetable = Timetable.objects.all()
    print("Timetable-to_json:full_timetable0", timetable[0])
    full = {}
    year = timetable[0].branch_subject.year.year
    full[year] = year
    time = str(timetable[0].time.starting_time) + '-' + str(timetable[0].time.ending_time)
    faculty = timetable[0].faculty.faculty_code
    room = timetable[0].room.room_number
    subject = timetable[0].branch_subject.subject.name
    day = timetable[0].day
    division = timetable[0].division
    branch = timetable[0].branch_subject.branch.branch

    faculty_json = {}
    room_json = {}
    time_json = {}
    subject_json = {}
    day_json = {}
    division_json = {}
    branch_json = {}
    year_json = {}
    faculty_json['faculty'] = faculty
    room_json['room'] = room
    print(subject)
    subject_json['subject'] = subject
    print(subject_json)
    time_json[time] = {json.dumps(faculty_json)}
    day_json[day] = time
    division_json[division] = day_json
    division_json = json.dumps(division_json)
    branch_json[branch]  = division_json
    year_json[year] = branch_json
    print(year_json)



    return HttpResponse(year_json.__str__())
