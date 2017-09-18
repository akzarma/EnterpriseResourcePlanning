from django.http import HttpResponse
from django.shortcuts import render

from General.models import CollegeExtraDetail, BranchSubject, FacultySubject
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

    divisions = CollegeExtraDetail.objects.filter(branch=branch_obj).values_list('division',flat=True)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    # form = TimetableForm()
    # branch = Branch.objects.all().values_list('branch', flat=True)
    room = Room.objects.filter(branch=branch_obj).values_list('room_number')
    print('Timetable-fill_timetable-rooms',room)
    print(branch)
    subjects_obj = BranchSubject.objects.filter(branch=branch_obj)
    subjects =[i.subject.name for i in subjects_obj]
    faculty = []
    print("Timetable:fill_timetable-subjects",subjects)
    context = {
        'branch': branch,
        'times': times,
        # 'form': form,
        'days': days,
        'division': divisions,
        'number_of_division': range(len(divisions)),
        'room':room,
        'subjects':subjects,
        'faculty' : faculty,
    }
    return render(request, 'fill_timetable.html', context)


def get_faculty(request):
    subject = request.POST.get('subject')
    faculty = FacultySubject.objects.get(subject=Subject.objects.get(subject=subject))
    print("TT:Faculty",faculty)
    return HttpResponse(faculty)