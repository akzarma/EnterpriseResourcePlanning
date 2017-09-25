import json

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

from General.models import CollegeExtraDetail, BranchSubject, FacultySubject, CollegeYear
# from .forms import TimetableForm
from Registration.models import Branch, Subject, Faculty
from .models import Time, Room, Timetable


# Create your views here.

def fill_timetable(request):
    times = []
    years = []
    # branch = Branch.objects.all()
    branch_obj = Branch.objects.get(branch='Computer')
    branch = branch_obj.branch
    for i in Time.objects.all():
        times.append(i.__str__())

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
            faculty.append((each.faculty.user.first_name + '-' +each.faculty.faculty_code))
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
            if not (str(key).__contains__("_room_choices") or str(key).__contains__("_faculty") or str(key).__contains__('csrfmiddlewaretoken')):
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

                faculty = Faculty.objects.get(faculty_code=selected_list.get(key+'_faculty'))

                room = Room.objects.get(room_number=selected_list.get(key+'_room_choices'))


                timetable = Timetable(room=room, faculty=faculty, division=division, branch_subject=branch_subject,
                                      time=time, day=day)
                timetable.save()



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




        return HttpResponse('Saved')
    else:
        return HttpResponse('Not Post')
