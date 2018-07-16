from django.contrib import admin

# Register your models here.
from Exam.models import ExamMaster, ExamDetail, ExamSubject, ExamGroup, ExamGroupDetail, ExamSubjectStudentRoom, \
    ExamSubjectRoom

admin.site.register(ExamMaster)
admin.site.register(ExamDetail)
admin.site.register(ExamSubject)
admin.site.register(ExamGroup)
admin.site.register(ExamGroupDetail)
admin.site.register(ExamSubjectStudentRoom)
admin.site.register(ExamSubjectRoom)
# admin.site.register(ExamGroupDetail)