# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-18 22:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Timetable', '0006_timetable_division'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='division',
            field=models.CharField(max_length=10),
        ),
    ]