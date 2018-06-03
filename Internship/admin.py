from django.contrib import admin

# Register your models here.
from General.models import StudentInternship
from Internship.models import Internship

admin.site.register(Internship)
admin.site.register(StudentInternship)