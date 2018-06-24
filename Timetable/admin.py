from django.contrib import admin
from .models import Timetable, Time, Room, DateTimetable

admin.site.register(Timetable)
admin.site.register(Time)
admin.site.register(Room)
admin.site.register(DateTimetable)
# admin.site.register(Batch)
