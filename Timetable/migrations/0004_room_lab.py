# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-18 16:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Timetable', '0003_auto_20170918_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='lab',
            field=models.BooleanField(default=True),
        ),
    ]
