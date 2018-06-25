from django.contrib import admin

# Register your models here.
from Exam.models import ExamMaster, ExamDetail, ExamSubject, ExamGroup, ExamGroupDetail

admin.site.register(ExamMaster)
admin.site.register(ExamDetail)
admin.site.register(ExamSubject)
admin.site.register(ExamGroup)
admin.site.register(ExamGroupDetail)