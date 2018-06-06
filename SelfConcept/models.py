from django.db import models

# Create your models here.
from Registration.models import Student


class Question(models.Model):
    question = models.CharField(max_length=600)
    is_negative_question = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question


class Answer(models.Model):
    answer = models.CharField(max_length=20)  # can be 'SA', 'A', 'U', 'D', 'SD'
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student = models.ForeignKey(Student)

    def __str__(self):
        return str(self.student) + ' **' + self.answer + '** ' + str(self.question)
