from django.http import HttpResponse
from django.shortcuts import render

from General.models import CollegeExtraDetail, BranchSubject, FacultySubject, CollegeYear
# from .forms import TimetableForm
from Registration.models import Branch, Subject
from .models import Time, Room


# Create your views here.

def fill_timetable(request):
    times = []
    # branch = Branch.objects.all()
    branch_obj = Branch.objects.get(branch='Computer')
    branch = branch_obj.branch
    for i in Time.objects.all():
        times.append(i)

    divisions = CollegeExtraDetail.objects.filter(branch=branch_obj).values_list('division', flat=True)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    # form = TimetableForm()
    # branch = Branch.objects.all().values_list('branch', flat=True)
    room = Room.objects.filter(branch=branch_obj).values_list('room_number')
    print('Timetable-fill_timetable-rooms', room)
    print(branch)
    subjects_obj = BranchSubject.objects.filter(branch=branch_obj)
    subjects = [i.subject.name for i in subjects_obj]
    faculty = []
    print("Timetable:fill_timetable-subjects", subjects)
    context = {
        'branch': branch,
        'times': times,
        # 'form': form,
        'days': days,
        'division': divisions,
        'number_of_division': range(len(divisions)),
        'room': room,
        'subjects': subjects,
        'faculty': faculty,
    }
    return render(request, 'fill_timetable.html', context)


def get_faculty(request):
    if request.is_ajax():
        subject = request.POST.get('subject')
        division = request.POST.get('division')
        print("Subject:", subject)
        print('division', division)
        subject_obj = Subject.objects.get(name=subject)
        # faculty_subject = FacultySubject.objects.filter(subject=subject_obj).filter(division=division)
        # faculty = []
        # for each in faculty_subject:
        #     faculty.append(each.faculty.first_name)
        branch_obj = Branch.objects.get(branch='Computer')
        year_obj = CollegeYear.objects.get(year='TE')
        college_obj = CollegeExtraDetail.objects.filter(branch=branch_obj).filter(year=year_obj).filter(
            division=division)
        faculty_subject = FacultySubject.objects.filter(division=college_obj).filter(subject=subject_obj)
        faculty = []
        for each in faculty_subject:
            faculty.append(each.faculty.first_name)
        print('Timetable-get_faculty:faculty', faculty)
        return HttpResponse(faculty)
