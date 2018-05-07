# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-25 19:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Registration', '0027_auto_20180425_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='course_pattern',
            field=models.IntegerField(default=2015),
        ),
        migrations.AddField(
            model_name='subject',
            name='elective_group',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='subject',
            name='is_elective',
            field=models.BooleanField(default=False),
        ),
    ]