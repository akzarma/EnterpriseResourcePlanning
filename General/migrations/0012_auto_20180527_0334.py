# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-26 22:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('General', '0011_auto_20180527_0334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='semester',
            name='lecture_end_date',
        ),
        migrations.RemoveField(
            model_name='semester',
            name='lecture_start_date',
        ),
    ]
