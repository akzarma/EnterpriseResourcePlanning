# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-19 14:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Registration', '0023_student_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentrollnumber',
            name='student',
        ),
        migrations.DeleteModel(
            name='StudentRollNumber',
        ),
    ]