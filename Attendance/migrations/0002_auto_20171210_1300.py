# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-10 13:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('General', '0001_initial'),
        ('Attendance', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='division',
            name='faculty',
        ),
        migrations.RemoveField(
            model_name='division',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='studentattendance',
            name='division',
        ),
        migrations.RemoveField(
            model_name='studentattendance',
            name='subject',
        ),
        migrations.AddField(
            model_name='studentattendance',
            name='faculty_subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='General.FacultySubject'),
        ),
        migrations.DeleteModel(
            name='Division',
        ),
    ]
