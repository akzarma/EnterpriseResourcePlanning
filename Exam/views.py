from django.shortcuts import render
import datetime

# Create your views here.
from Exam.models import ExamMaster


def exam_register(request):
    if request.method == 'GET':
        return render(request,'exam_register.html')

    else:
        exam_name = request.POST.get('exam_name')
        ExamMaster.objects.create(exam_name=exam_name,start_date=datetime.date.today())
        context = {'success':"Successfully registered"}
        return render(request,'exam_register.html',context)