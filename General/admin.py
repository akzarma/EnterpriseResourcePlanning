from django.contrib import admin
from .models import StudentDivision, StudentSubject, BranchSubject, CollegeYear, Semester, CollegeExtraDetail, Shift, \
    FacultySubject, Batch, SemesterPeriod

# Register your models here.

admin.site.register(StudentDivision)
admin.site.register(StudentSubject)
admin.site.register(BranchSubject)
admin.site.register(CollegeYear)
admin.site.register(Semester)
admin.site.register(FacultySubject)
admin.site.register(CollegeExtraDetail)
admin.site.register(Shift)
admin.site.register(Batch)
admin.site.register(SemesterPeriod)
