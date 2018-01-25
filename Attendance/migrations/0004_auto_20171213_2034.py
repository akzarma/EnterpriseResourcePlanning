# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-13 20:34
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('Timetable', '0002_timetable_is_practical'),
        ('Attendance', '0003_auto_20171210_1301'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailyattendance',
            name='attendance',
        ),
        migrations.RemoveField(
            model_name='studentattendance',
            name='faculty_subject',
        ),
        migrations.AddField(
            model_name='studentattendance',
            name='attended',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='studentattendance',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='studentattendance',
            name='timetable',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Timetable.Timetable'),
        ),
        migrations.DeleteModel(
            name='DailyAttendance',
        ),
    ]
