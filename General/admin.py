from django.contrib import admin
from .models import StudentDetail, StudentSubject, BranchSubject, CollegeYear, Semester, Shift, \
    FacultySubject, Batch, Division, YearBranch, Schedule, Schedulable, YearSemester, ElectiveDivision, ElectiveBatch

# Register your models here.

admin.site.register(StudentDetail)
admin.site.register(StudentSubject)
admin.site.register(BranchSubject)
admin.site.register(CollegeYear)
admin.site.register(Semester)
admin.site.register(FacultySubject)
admin.site.register(Division)
admin.site.register(YearBranch)
admin.site.register(Shift)
admin.site.register(Batch)
admin.site.register(Schedule)
admin.site.register(Schedulable)
admin.site.register(YearSemester)
admin.site.register(ElectiveDivision)
admin.site.register(ElectiveBatch)
# admin.site.register(SemesterPeriod)
