from django.shortcuts import render, redirect

# Create your views here.
from Registration.views import has_role
from SelfConcept.models import Question, Answer


def test(request):
    user = request.user
    if not user.is_anonymous:
        if has_role(user, 'student'):
            student = user.student
            if request.method == 'GET':
                if Answer.objects.filter(student=student):
                    return render(request, 'test_page.html',
                              {'info': 'You have already given the test.'})
                else:
                    all_questions = Question.objects.filter(is_active=True)
                    return render(request, 'test_page.html',
                                  {'all_questions': all_questions})
            if request.method == 'POST':
                all_questions = Question.objects.filter(is_active=True)

                for each_question in all_questions:
                    answer_str = request.POST.get('option_' + str(each_question.pk))  # SA A D SD U
                    answer_obj = Answer.objects.get_or_create(student=student, question=each_question)[0]
                    answer_obj.answer = answer_str
                    answer_obj.save()
                return render(request, 'test_page.html', {'success': 'You have given the test successfully.'})
        else:
            return render(request, 'test_page.html', {'error': 'You must be a student to give the test.'})

    else:
        return redirect('/login/')
