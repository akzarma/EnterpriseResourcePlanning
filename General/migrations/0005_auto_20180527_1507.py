# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-27 09:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('General', '0004_merge_20180527_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentdetail',
            name='roll_number',
            field=models.PositiveIntegerField(null=True),
        ),
    ]