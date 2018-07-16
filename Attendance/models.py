# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models

from General.models import FacultySubject, StudentDetail
from Registration.models import Student, Subject, Faculty

# Contains
# StudentAttendance - Relation(Student,Subject) + attendance details
# Daily Attendance - date,time,attended(Derived from student attendance)
from Timetable.models import Timetable, DateTimetable


class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    timetable = models.ForeignKey(DateTimetable, on_delete=models.CASCADE, null=True)  # Should not be null
    attended = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.student.first_name + self.student.gr_number


class SubjectLectures(models.Model):
    faculty_subject = models.ForeignKey(FacultySubject,on_delete=models.CASCADE)
    conducted_lectures = models.IntegerField(default=0)


class StudentSubjectTotalAttendance(models.Model):
    student =models.ForeignKey(Student,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    attended = models.IntegerField(default=0)

# class DailyAttendance(models.Model):
#     date = models.DateTimeField()
#     # time = models.TimeField()
#     attended = models.BooleanField()
#     attendance = models.ForeignKey(StudentAttendance)


class FacultyAttendance(models.Model):
    faculty = models.OneToOneField(Faculty,on_delete=models.CASCADE)
    in_time = models.TimeField()
    out_time = models.TimeField()

