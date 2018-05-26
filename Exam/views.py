import json

from django.http import HttpResponse
from django.shortcuts import render
import datetime

# Create your views here.
from Exam.forms import ExamDetailForm
from Exam.models import ExamMaster, ExamSubject
from General.models import Semester, BranchSubject, CollegeYear, YearBranch
from Registration.models import Branch


def exam_register(request):
    if request.method == 'GET':
        return render(request, 'exam_register.html')

    else:
        exam_name = request.POST.get('exam_name')
        ExamMaster.objects.create(exam_name=exam_name, start_date=datetime.date.today())
        context = {'success': "Successfully registered"}
        return render(request, 'exam_register.html', context)


def exam_detail(request):
    if request.method == "GET":
        return render(request, 'exam_detail.html', {'form': ExamDetailForm})
    else:
        form = ExamDetailForm(request.POST)
        if form.is_valid():
            exam_detail_obj = form.save()
            subjects = request.POST.getlist('subject')

            for each_subject in subjects:
                subject = BranchSubject.objects.get(is_active=True, year_branch=exam_detail_obj.year,
                                                    subject__short_form=each_subject).subject
                ExamSubject.objects.create(exam=exam_detail_obj, subject=subject)

            return render(request, 'exam_detail.html', {
                'success': 'Successfully done.'
            })
        else:
            return render(request, 'exam_detail.html', {
                'form': form,
                'error': 'Not valid'
            })


def get_subjects(request):
    if request.is_ajax():
        if request.method == "POST":
            year = request.POST.get('year')
            semester = request.POST.get('semester')
            semester_obj = Semester.objects.get(pk=semester)
            # year_splitted = year.split(' ')
            # branch = year_splitted[0]
            # year = year_splitted[1]
            # branch_obj = Branch.objects.get(branch=branch)
            # year_obj = CollegeYear.objects.get(year=year)
            year_branch_obj = YearBranch.objects.get(pk=year)

            subjects = BranchSubject.objects.filter(year_branch=year_branch_obj, semester=semester_obj).values_list(
                'subject__short_form', flat=True)
            return HttpResponse(json.dumps(list(subjects)))

        else:
            return HttpResponse("Not post")
    else:
        return HttpResponse('Not ajax')
