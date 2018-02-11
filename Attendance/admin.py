# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import StudentAttendance, TotalAttendance

# Register your models here.

admin.site.register(StudentAttendance)
admin.site.register(TotalAttendance)
