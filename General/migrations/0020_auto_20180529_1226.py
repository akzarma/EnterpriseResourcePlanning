# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-29 06:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('General', '0019_studentdetail_has_registered_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='electivegroup',
            name='no_of_sub_to_choose',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='studentdetail',
            name='roll_number',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]