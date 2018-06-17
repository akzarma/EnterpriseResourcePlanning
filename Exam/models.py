from django.db import models

# Create your models here.
from General.models import Division, Semester, StudentSubject, YearBranch
from Registration.models import Subject, Faculty
from Timetable.models import Room


class ExamMaster(models.Model):
    exam_name = models.CharField(max_length=300)
    # Below 2 fields would be filled ate the time of active/inactive
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.exam_name


class ExamDetail(models.Model):
    exam = models.ForeignKey(ExamMaster)
    year = models.ForeignKey(YearBranch, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    schedule_start_date = models.DateField()
    schedule_end_date = models.DateField()
    is_active = models.BooleanField(default=True)


class ExamSubject(models.Model):
    exam = models.ForeignKey(ExamDetail, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    coordinator = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class ExamGroup(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)


class ExamGroupDetail(models.Model):
    exam_group = models.ForeignKey(ExamGroup, on_delete=models.CASCADE)
    exam = models.ForeignKey(ExamDetail, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class ExamGroupRoom(models.Model):
    exam_group = models.ForeignKey(ExamGroup, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class Mark(models.Model):
    exam = models.ForeignKey(ExamDetail, on_delete=models.CASCADE)
    student_subject = models.ForeignKey(StudentSubject, on_delete=models.CASCADE)
    max_total = models.IntegerField()


class MarksType(models.Model):
    type_of_marks = models.CharField(max_length=200)
    marks = models.ForeignKey(Mark, on_delete=models.CASCADE)
    marks_obtained = models.IntegerField()
    max_marks = models.PositiveIntegerField()
    cut_off_marks = models.IntegerField(default=0)
