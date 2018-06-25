from django.contrib import admin

# Register your models here.
from Feedback.models import FormMaster, Question, Answer, StudentForm, FormAnswer, StudentAnswer

admin.site.register(FormMaster)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(StudentForm)
admin.site.register(FormAnswer)
admin.site.register(StudentAnswer)