from django.http import HttpResponse
from django.shortcuts import render
from .forms import TimetableForm
from Registration.models import Branch
from .models import Time


# Create your views here.

def fill_timetable(request):
    times = []

    for i in Time.objects.all():
        times.append(i)

    division_list = ['A', 'B', 'C']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    form = TimetableForm()
    branch = Branch.objects.all().values_list('branch', flat=True)
    print(branch)
    context = {
        'branch': branch,
        'times': times,
        'form': form,
        'days': days,
        'division': division_list,
        'number_of_division': range(len(division_list)),
    }
    return render(request, 'fill_timetable.html', context)
