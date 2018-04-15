# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models

from General.models import FacultySubject
from Registration.models import Student, Subject, Faculty

# Contains
# StudentAttendance - Relation(Student,Subject) + attendance details
# Daily Attendance - date,time,attended(Derived from student attendance)
from Timetable.models import Timetable, DateTimetable


class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    timetable = models.ForeignKey(DateTimetable, on_delete=models.CASCADE,null=True)#Should not be null
    attended = models.BooleanField(default=False)

    def __str__(self):
        return self.student.first_name + self.student.gr_number


# class DailyAttendance(models.Model):
#     date = models.DateTimeField()
#     # time = models.TimeField()
#     attended = models.BooleanField()
#     attendance = models.ForeignKey(StudentAttendance)


class FacultyAttendance(models.Model):
    faculty = models.OneToOneField(Faculty)
    in_time = models.TimeField()
    out_time = models.TimeField()


class TotalAttendance(models.Model):
    student = models.ForeignKey(Student)
    subject = models.ForeignKey(Subject)
    total_lectures = models.PositiveIntegerField()
    attended_lectures = models.PositiveIntegerField()

    def __str__(self):
        return self.student.first_name + self.student.gr_number + self.subject.name
