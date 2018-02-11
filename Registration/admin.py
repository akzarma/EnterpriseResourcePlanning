# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Subject, Student, Faculty, Branch,StudentRollNumber

# Register your models here.
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Faculty)
admin.site.register(Branch)
admin.site.register(StudentRollNumber)
