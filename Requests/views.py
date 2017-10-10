from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from Timetable.models import Room


def vacant_room(request):
    if request.method == 'POST':
        day = request.POST.get('day_field')
        time = request.POST.get('time_field')
        rooms = list(Room.objects.filter().values_list('room_number', flat=True))
        return HttpResponse(str(rooms))
    return "None"