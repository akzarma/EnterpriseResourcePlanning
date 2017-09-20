import json

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from General.models import CollegeExtraDetail, BranchSubject, FacultySubject, CollegeYear
# from .forms import TimetableForm
from Registration.models import Branch, Subject
from .models import Time, Room


# Create your views here.

def fill_timetable(request):
    times = []
    years = []
    # branch = Branch.objects.all()
    branch_obj = Branch.objects.get(branch='Computer')
    branch = branch_obj.branch
    for i in Time.objects.all():
        times.append(i)

    for i in CollegeYear.objects.all().values_list('year',flat=True):
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


def get_subject(request):
    year = request.POST.get('year')
    subjects = BranchSubject.objects.filter(year=CollegeYear.objects.get(year=year))
    subject_list = [i.subject.name for i in subjects]
    subject_string = ",".join(subject_list)
    return HttpResponse(subject_string)