from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from Timetable.models import Room, Timetable

# Create your views here.

@csrf_exempt
def vacant_room(request):
    if request.method == 'POST':
        day = request.POST.get('day_field')
        time = request.POST.get('time_field')
        timetable_set_rooms = set(Timetable.objects.filter(time__starting_time=time, day=day).values_list('room__room_number', flat=True))
        print("TTTTTTTTTT",timetable_set_rooms)
        rooms = set(Room.objects.filter().values_list('room_number', flat=True))
        print("RRRRRRRRROOMs",rooms)
        return HttpResponse(str(rooms-timetable_set_rooms))
    return HttpResponse("None")