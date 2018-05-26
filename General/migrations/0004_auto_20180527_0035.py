# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-26 19:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('General', '0003_yearsemester'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='semester',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='semester',
            name='start_date',
        ),
        migrations.AddField(
            model_name='yearsemester',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='yearsemester',
            name='start_date',
            field=models.DateField(null=True),
        ),
    ]
