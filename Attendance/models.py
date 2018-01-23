# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import  datetime

from django.db import models

from General.models import FacultySubject
from Registration.models import Student, Subject, Faculty


# Contains
# StudentAttendance - Relation(Student,Subject) + attendance details
# Daily Attendance - date,time,attended(Derived from student attendance)
from Timetable.models import Timetable


class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    # faculty_subject = models.ForeignKey(FacultySubject)
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)
    date = models.DateField(null=True)#Should not be null=True
    # time = models.TimeField()
    attended = models.BooleanField(default=False)

    def __str__(self):
        return self.student.first_name


# class DailyAttendance(models.Model):
#     date = models.DateTimeField()
#     # time = models.TimeField()
#     attended = models.BooleanField()
#     attendance = models.ForeignKey(StudentAttendance)


class FacultyAttendance(models.Model):
    faculty = models.OneToOneField(Faculty)
    in_time = models.TimeField()
    out_time = models.TimeField()
