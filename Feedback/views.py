import os

import xlsxwriter
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from Feedback.models import Question, FormMaster, FormAnswer, StudentForm, Answer, StudentAnswer
from General.models import Division, CollegeYear, YearBranch, StudentDetail
from Registration.models import Branch, Student
from Registration.views import has_role


def self_concept(request):
    user = request.user
    form = FormMaster.objects.get(form_name='Self Concept', is_active=True)
    if not user.is_anonymous:
        if has_role(user, 'student'):
            student = user.student
            all_questions = Question.objects.filter(form=form, is_active=True)
            if request.method == 'GET':
                try:
                    student_form = StudentForm.objects.get(student=student, form=form, is_active=True)
                except:
                    form_answers = FormAnswer.objects.filter(form=form, is_active=True)
                    return render(request, 'test_page.html',
                                  {'all_questions': all_questions,
                                   'form_answers': form_answers})
                return render(request, 'test_page.html', {
                    'error': 'You have already given the test. Your Score was ' + str(student_form.score)})
            if request.method == 'POST':
                student_form = StudentForm.objects.get_or_create(student=student, form=form, is_active=True)[0]
                for each in all_questions:
                    # try:
                    answer_obj = Answer.objects.get(pk=int(request.POST.get('option_' + str(each.pk))))
                    # except:

                    student_answer_obj = StudentAnswer.objects.get_or_create(student_form=student_form,
                                                                             question=each)[0]
                    student_answer_obj.answer = answer_obj
                    student_answer_obj.save()

                score = 0
                for each_student_answer in StudentAnswer.objects.filter(student_form=student_form):
                    if each_student_answer.question.is_negative_question:
                        score += each_student_answer.answer.negative_que_score
                    else:
                        score += each_student_answer.answer.positive_que_score
                student_form.score = score
                student_form.save()
                return render(request, 'test_page.html',
                              {'success': 'You have given the test successfully. Your Score is ' + str(score)})
        else:
            return render(request, 'test_page.html', {'error': 'You must be a student to give the test.'})

    else:
        return redirect('/login/')


def self_concept_result(request):
    class_active = "feedback"
    user = request.user
    form = FormMaster.objects.get(form_name='Self Concept', is_active=True)
    if not user.is_anonymous:
        if has_role(user, 'faculty'):
            if request.method == 'GET':

                timetable_json = {}

                college_extra_detail = Division.objects.all()

                for each in college_extra_detail:
                    branch = each.year_branch.branch.branch
                    year = each.year_branch.year.year
                    division = each.division

                    if branch in timetable_json:
                        if year in timetable_json[branch]:
                            {}
                        else:
                            timetable_json[branch][year] = []
                    else:
                        timetable_json[branch] = {}
                        timetable_json[branch][year] = []

                    timetable_json[branch][year].append(division)

                return render(request, 'select_class.html', {
                    'class_active': class_active,
                    'timetable': timetable_json
                })
            elif request.POST.get('select_class_button'):
                try:
                    year_obj = CollegeYear.objects.get(year=request.POST.get('year'))
                    branch_obj = Branch.objects.get(branch=request.POST.get('branch'))
                    year_branch_obj = YearBranch.objects.get(year=year_obj,
                                                             branch=branch_obj,
                                                             is_active=True)
                    division_obj = Division.objects.get(year_branch=year_branch_obj,
                                                        division=request.POST.get('division'),
                                                        is_active=True)

                except Exception as e:
                    return render(request, 'select_class.html', {'error': e})
                given_list = {}
                for each in StudentAnswer.objects.filter(student_form__form=form).values_list('student_form__student',
                                                                                              flat=True).distinct():
                    if each not in given_list:
                        given_list[each] = StudentForm.objects.get(student=Student.objects.get(pk=each)).score
                students = StudentDetail.objects.filter(batch__division=division_obj,
                                                        is_active=True).order_by('student__gr_number')

                return render(request, 'student_list.html',
                              {'students': students,
                               'class_active': class_active,
                               'given_list': given_list,
                               'year': year_obj.year,
                               'branch': branch_obj.branch,
                               'division': division_obj.division})

            elif request.POST.get('result_button'):
                student_detail = StudentDetail.objects.get(pk=int(request.POST.get('result_button')))
                student_form = StudentForm.objects.get(student=student_detail.student,
                                                       form=form,
                                                       is_active=True)
                result_pos = {}
                result_neg = {}
                for each_answer in FormAnswer.objects.filter(form=form, is_active=True):
                    if each_answer.answer.answer not in result_pos:
                        result_pos[each_answer.answer.answer] = 0
                    if each_answer.answer.answer not in result_neg:
                        result_neg[each_answer.answer.answer] = 0
                form_answers = FormAnswer.objects.filter(form=form, is_active=True)
                for each_student_answer in StudentAnswer.objects.filter(student_form=student_form):
                    # each_student_answer = StudentAnswer(each_student_answer)

                    if each_student_answer.question.is_negative_question:
                        if each_student_answer.answer.answer not in result_neg:
                            result_neg[each_student_answer.answer.answer] = 0
                        result_neg[each_student_answer.answer.answer] += 1
                    else:
                        if each_student_answer.answer.answer not in result_pos:
                            result_pos[each_student_answer.answer.answer] = 0
                        result_pos[each_student_answer.answer.answer] += 1

                return render(request, 'result.html', {'result_pos': result_pos,
                                                       'result_neg': result_neg,
                                                       'form_answers': form_answers,
                                                       'student': student_detail,
                                                       'score': student_form.score})

        else:
            return render(request, 'student_list.html', {'error': 'You must be faculty to see this page.'})
    else:
        return redirect('/login/')


def self_concept_pdf(request):
    class_active = "feedback"
    user = request.user
    form = FormMaster.objects.get(form_name='Self Concept', is_active=True)
    if not user.is_anonymous:
        if has_role(user, 'faculty'):
            if request.method == 'POST':
                year_obj = CollegeYear.objects.get(year=request.POST.get('year'))
                branch_obj = Branch.objects.get(branch=request.POST.get('branch'))
                year_branch_obj = YearBranch.objects.get(year=year_obj,
                                                         branch=branch_obj,
                                                         is_active=True)
                division_obj = Division.objects.get(year_branch=year_branch_obj,
                                                    division=request.POST.get('division'),
                                                    is_active=True)
                directory = './Media/documents/Feedback/' + year_obj.year + '/' + branch_obj.branch + \
                            '/' + division_obj.division + '/'
                prefix = 'Media/documents/Feedback/' + year_obj.year + '/' + branch_obj.branch + \
                            '/' + division_obj.division + '/'
                if not os.path.exists(directory):
                    os.makedirs(directory)
                filename = 'SelfConcept.xlsx'
                workbook = xlsxwriter.Workbook(directory + 'SelfConcept.xlsx')
                worksheet = workbook.add_worksheet()

                dark_gray = workbook.add_format()
                dark_gray.set_bg_color('#b2aeae')
                dark_gray.set_border(1)

                light_gray = workbook.add_format()
                light_gray.set_border(1)
                light_gray.set_bg_color('#f1eacf')

                given_list = {}
                for each in StudentAnswer.objects.filter(student_form__form=form).values_list('student_form__student',
                                                                                              flat=True).distinct():
                    if each not in given_list:
                        given_list[each] = StudentForm.objects.get(student=Student.objects.get(pk=each)).score
                students = StudentDetail.objects.filter(batch__division=division_obj,
                                                        is_active=True).order_by('student__gr_number')
                row = 3
                col = 3
                for each_student in students:
                    worksheet.write(row, col, each_student.student.gr_number, light_gray if row % 2 == 0 else dark_gray)
                    worksheet.write(row, col + 1,
                                    each_student.student.first_name + ' ' + each_student.student.last_name,
                                    light_gray if row % 2 == 0 else dark_gray)
                    if each_student.student.pk in given_list:
                        worksheet.write(row, col + 2, given_list[each_student.student.pk],
                                        light_gray if row % 2 == 0 else dark_gray)
                    else:
                        worksheet.write(row, col + 2, 'Not given', light_gray if row % 2 == 0 else dark_gray)
                    row += 1

                workbook.close()

                return redirect('/'+prefix + filename)
