# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models

# Contains
# Faculty (Entity)
# Student (Entity)
# Subject (Entity)
from UserModel.models import User


def faculty_directory_path(instance, filename):
    return 'Media/Faculty/{0}/{1}'.format(instance.faculty_code, filename)


# Create your models here.
class Faculty(models.Model):
    initials = models.CharField(max_length=10, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    faculty_code = models.CharField(max_length=15, primary_key=True)
    DOB = models.DateField(default='1996-02-11', blank=True, null=True)

    # account details
    salary = models.IntegerField(default=10, blank=True, null=True)

    # teaching
    teaching_from = models.DateField(default=datetime.now)
    subjects_experience = models.CharField(max_length=250)
    projects = models.TextField(max_length=300, null=True, blank=True)

    # personal details
    caste_type = models.CharField(max_length=20)
    # email = models.EmailField(max_length=100)
    mobile = models.BigIntegerField(default=0)
    religion = models.CharField(max_length=20)
    sub_caste = models.CharField(max_length=30)
    handicapped = models.BooleanField(default=0)
    nationality = models.CharField(max_length=50)

    # emergency contact
    emergency_name = models.CharField(max_length=50, null=True, blank=True)
    emergency_mobile = models.BigIntegerField(null=True, blank=True)
    emergency_relation = models.CharField(max_length=50, null=True, blank=True)
    emergency_address = models.CharField(max_length=100, null=True, blank=True)

    # family
    # father
    father_name = models.CharField(max_length=50, null=True, blank=True)
    father_profession = models.CharField(max_length=30, null=True, blank=True)
    father_designation = models.CharField(max_length=30, null=True, blank=True)
    father_mobile = models.BigIntegerField(blank=True, null=True)
    father_email = models.EmailField(blank=True, null=True)
    # mother
    mother_name = models.CharField(max_length=50, null=True, blank=True)
    mother_profession = models.CharField(max_length=30, null=True, blank=True)
    mother_designation = models.CharField(max_length=30, null=True, blank=True)
    mother_mobile = models.BigIntegerField(blank=True, null=True)
    mother_email = models.EmailField(null=True, blank=True)

    # permanent address
    permanent_address = models.CharField(max_length=100, blank=True, null=True)
    permanent_state = models.CharField(max_length=50, blank=True, null=True)
    permanent_city = models.CharField(max_length=50, blank=True, null=True)
    permanent_pin_code = models.PositiveIntegerField(blank=True, null=True)
    permanent_country = models.CharField(max_length=50, blank=True, null=True)

    # current address
    current_address = models.CharField(max_length=100, null=True, blank=True)
    current_state = models.CharField(max_length=50, null=True, blank=True)
    current_city = models.CharField(max_length=50, null=True, blank=True)
    current_pin_code = models.PositiveIntegerField(null=True, blank=True)
    current_country = models.CharField(max_length=50, null=True, blank=True)

    # documents

    doc = models.FileField(upload_to=faculty_directory_path, null=True, blank=True)
    doc_profile_pic = models.ImageField(upload_to=faculty_directory_path, null=True, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.faculty_code


def student_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    # "user_%d" % instance.owner.id, "car_%s" % instance.slug, filename
    return 'Media/Student/Student_{0}/{1}'.format(instance.gr_number, "test.jpg")


class Student(models.Model):
    # Basic Details
    key = models.CharField(max_length=40, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    DOB = models.DateField(default='1996-02-11')

    admission_type = models.CharField(max_length=50)
    shift = models.CharField(max_length=1)
    caste_type = models.CharField(max_length=20)
    branch = models.CharField(max_length=50)
    gr_number = models.CharField(max_length=15, primary_key=True)
    programme = models.CharField(max_length=10)
    # personal details
    mobile = models.BigIntegerField(default=0)
    religion = models.CharField(max_length=20, blank=True, null=True)
    sub_caste = models.CharField(max_length=30, null=True, blank=True)
    handicapped = models.BooleanField(default=0)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    # family
    # father
    father_name = models.CharField(max_length=50, null=True, blank=True)
    father_profession = models.CharField(max_length=30, null=True, blank=True)
    father_designation = models.CharField(max_length=30, null=True, blank=True)
    father_mobile = models.BigIntegerField(default=0, null=True, blank=True)
    father_email = models.EmailField(max_length=100, null=True, blank=True)

    # mother
    mother_name = models.CharField(max_length=50, null=True, blank=True)
    mother_profession = models.CharField(max_length=30, null=True, blank=True)
    mother_designation = models.CharField(max_length=30, null=True, blank=True)
    mother_mobile = models.BigIntegerField(default=0, null=True, blank=True)
    mother_email = models.EmailField(null=True, blank=True)

    # emergency contact
    emergency_name = models.CharField(max_length=50, null=True, blank=True)
    emergency_mobile = models.BigIntegerField(null=True, blank=True)
    emergency_relation = models.CharField(max_length=50, null=True, blank=True)
    emergency_address = models.CharField(max_length=100, null=True, blank=True)

    # permanent address
    permanent_address = models.CharField(max_length=100, blank=True, null=True)
    permanent_state = models.CharField(max_length=50, blank=True, null=True)
    permanent_city = models.CharField(max_length=50, blank=True, null=True)
    permanent_pin_code = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    permanent_country = models.CharField(max_length=50, blank=True, null=True)

    # current address
    current_address = models.CharField(max_length=100, null=True, blank=True)
    current_state = models.CharField(max_length=50, null=True, blank=True)
    current_city = models.CharField(max_length=50, null=True, blank=True)
    current_pin_code = models.IntegerField(null=True, blank=True)
    current_country = models.CharField(max_length=50, null=True, blank=True)

    # Exam details
    jee_physics = models.PositiveIntegerField(default=0, null=True, blank=True)
    jee_maths = models.PositiveIntegerField(default=0, null=True, blank=True)
    jee_chemistry = models.PositiveIntegerField(default=0, null=True, blank=True)
    jee_total = models.PositiveIntegerField(default=0, null=True, blank=True)
    jee_max_physics = models.PositiveIntegerField(default=0, null=True, blank=True)
    jee_max_maths = models.PositiveIntegerField(default=0, null=True, blank=True)
    jee_max_chemistry = models.PositiveIntegerField(default=0, null=True, blank=True)

    # documents
    doc_tenth_marksheet = models.FileField(upload_to=student_directory_path, null=True, blank=True)
    doc_twelfth_marksheet = models.FileField(upload_to=student_directory_path, null=True, blank=True)
    doc_jee_marksheet = models.FileField(upload_to=student_directory_path, null=True, blank=True)
    doc_profile_pic = models.ImageField(upload_to=student_directory_path, null=True, blank=True)

    def __str__(self):
        return self.first_name + ' ' + str(self.pk)


class Subject(models.Model):
    code = models.CharField(max_length=20, primary_key=True, blank=True)
    name = models.CharField(max_length=100)
    short_form = models.CharField(max_length=10)
    is_practical = models.BooleanField(default=False)
    # semester = models.IntegerField(default=1)
    credits = models.IntegerField(default=0, blank=True)
    # elective_group = models.IntegerField(default=1,null=True, blank=True)
    course_pattern = models.IntegerField(default=2015, blank=True)
    is_elective_group = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Elective(models.Model):
    name = models.CharField(max_length=100)
    short_form = models.CharField(max_length=10)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.subject) + ' '+ self.name

class Branch(models.Model):
    branch = models.CharField(max_length=50)

    # is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.branch)

# Removing HOD table(Should be added in rolemanager)
# class HOD(models.Model):
#     faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
#     branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
#     start_date = models.DateField(blank=True)
#     end_date = models.DateField(null=True, blank=True)
#     is_active = models.BooleanField(default=True)

# def __str__(self):
# return str(self.faculty) + str(self.branch)

# class StudentRollNumber(models.Model):
#     student = models.ForeignKey(Student)
#     roll_number = models.IntegerField()
#     is_active = models.BooleanField(default=True)
#
#     def __str__(self):
#         return str(self.student.gr_number) + ' ' + str(self.roll_number) + ' ' + str(self.student.first_name)
