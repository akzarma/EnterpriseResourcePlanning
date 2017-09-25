import json

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from General.models import CollegeExtraDetail, BranchSubject, FacultySubject, CollegeYear
# from .forms import TimetableForm
from Registration.models import Branch, Subject
from .models import Time, Room, Timetable


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


def get_subject(request):
    year = request.POST.get('year')
    subjects = BranchSubject.objects.filter(year=CollegeYear.objects.get(year=year))
    subject_list = [i.subject.name for i in subjects]
    subject_string = ",".join(subject_list)
    return HttpResponse(subject_string)


def save_timetable(request):
    if request.method == 'POST':
        print(request.POST.get)
        return HttpResponse('Saved')
    else:
        return HttpResponse('Not Post')


def to_json(request):
    full_timetable = Timetable.objects.all()
    answer = {}
    time = {}
    day = {}
    division = {}
    branch = {}
    year = {}
    output = ""
    # key = {}
    # key['test'] = 'inner'
    # key['test']['inner'] = 'hello'
    # print(key)

    for year in full_timetable.values_list('branch_subject__year__year', flat=True):
        print("year", year)
        branch_filtered = full_timetable.filter(
            branch_subject=BranchSubject.objects.filter(year=CollegeYear.objects.get(year=year)))
        for branch in branch_filtered.values_list(
                'branch_subject__branch__branch', flat=True):
            print('branch', branch)
            division_filtered = branch_filtered.filter(
                branch_subject=BranchSubject.objects.filter(branch=Branch.objects.get(
                    branch=branch)))
            for division in division_filtered.values_list('division', flat=True):
                print('division', division)
                day_filtered = division_filtered.filter(division=division)
                for day in day_filtered.values_list('day', flat=True):
                    print('day', day)
                    time_filtered = day_filtered.filter(day=day)
                    for time in time_filtered.values_list('time', flat=True):
                        print('time', time.__str__())


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
    return HttpResponse(output)

# {"800-900": {"subject": "Database Management Systems", "room": "B-101", "faculty": "Yogesh"}, "1315-1415": {"subject": "Database Management Systems", "room": "B-101", "faculty": "Yogesh"}}
# ,{"800-900": {"subject": "Software Engineering and Project Management", "room": "B-202", "faculty": "Nitin"}, "900-1000": {"subject": "Software Engineering and Project Management", "room": "B-202", "faculty": "Nitin"}, "1315-1415": {"subject": "Software Engineering and Project Management", "room": "B-202", "faculty": "Nitin"}}
