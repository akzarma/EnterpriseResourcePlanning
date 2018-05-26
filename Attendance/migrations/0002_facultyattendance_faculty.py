# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-26 14:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Registration', '0028_auto_20180426_0036'),
        ('Attendance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='facultyattendance',
            name='faculty',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='Registration.Faculty'),
        ),
    ]