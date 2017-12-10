# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from General.models import FacultySubject
from Registration.models import Student, Subject, Faculty


# Contains
# StudentAttendance - Relation(Student,Subject) + attendance details
# Daily Attendance - date,time,attended(Derived from student attendance)


class StudentAttendance(models.Model):
    student = models.ForeignKey(Student)
    faculty_subject = models.ForeignKey(FacultySubject)

    def __str__(self):
        return self.student.first_name + self.faculty_subject.subject.name + self.faculty_subject.division.division


class DailyAttendance(models.Model):
    date = models.DateTimeField()
    # time = models.TimeField()
    attended = models.BooleanField()
    attendance = models.ForeignKey(StudentAttendance)


class FacultyAttendance(models.Model):
    faculty = models.OneToOneField(Faculty)
    in_time = models.TimeField()
    out_time = models.TimeField()
