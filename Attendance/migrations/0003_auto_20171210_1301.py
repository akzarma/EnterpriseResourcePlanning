# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-10 13:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance', '0002_auto_20171210_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentattendance',
            name='faculty_subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='General.FacultySubject'),
        ),
    ]