from django.db import models

# Create your models here.
from Registration.models import Student


class FormMaster(models.Model):
    form_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.form_name


class Question(models.Model):
    form = models.ForeignKey(FormMaster, on_delete=models.CASCADE)
    question = models.CharField(max_length=500)
    is_negative_question = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.form.form_name + ' ' + self.question


class Answer(models.Model):
    answer = models.CharField(max_length=30)
    positive_que_score = models.IntegerField()
    negative_que_score = models.IntegerField()

    def __str__(self):
        return self.answer + ' pos score: ' + str(self.positive_que_score) + ' neg score: ' + str(
            self.negative_que_score)


class StudentForm(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    form = models.ForeignKey(FormMaster)
    score = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.student) + ' ' + str(self.form)


class FormAnswer(models.Model):
    form = models.ForeignKey(FormMaster, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.form.form_name + ' ' + self.answer.answer


class StudentAnswer(models.Model):
    student_form = models.ForeignKey(StudentForm, on_delete=models.CASCADE)
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(Answer, null=True)

    def __str__(self):
        return str(self.student_form) + ' ' + str(self.answer) + ' ' + str(self.question)
