# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-23 15:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Registration', '0009_auto_20171214_1913'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faculty',
            name='DOB',
        ),
    ]
