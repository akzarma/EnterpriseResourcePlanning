# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-19 14:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('General', '0007_studentdivision_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='batch',
            name='ending_roll_number',
        ),
        migrations.RemoveField(
            model_name='batch',
            name='starting_roll_number',
        ),
    ]
