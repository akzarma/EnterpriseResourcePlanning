# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-14 06:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Registration', '0004_auto_20171005_0702'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='semester',
            field=models.IntegerField(default=1),
        ),
    ]