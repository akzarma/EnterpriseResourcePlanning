# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-18 15:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Research', '0003_auto_20171018_0747'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paper',
            name='is_conference',
        ),
        migrations.AlterField(
            model_name='paper',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 10, 18, 15, 23, 17, 963207)),
        ),
    ]