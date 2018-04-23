# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-23 14:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Attendance', '0001_initial'),
        ('Timetable', '0001_initial'),
        ('Registration', '0026_remove_subject_semester'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentattendance',
            name='timetable',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Timetable.DateTimetable'),
        ),
        migrations.AddField(
            model_name='facultyattendance',
            name='faculty',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Registration.Faculty'),
        ),
    ]