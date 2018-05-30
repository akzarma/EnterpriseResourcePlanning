from django.contrib import admin

# Register your models here.
from Dashboard.models import SpecificNotification, GeneralStudentNotification, GeneralFacultyNotification

admin.site.register(SpecificNotification)
admin.site.register(GeneralStudentNotification)
admin.site.register(GeneralFacultyNotification)