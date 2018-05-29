# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-29 15:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('General', '0021_auto_20180529_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='electivegroup',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='electivegroup',
            name='no_of_sub_to_choose',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentdetail',
            name='last_subject_registration_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentsubject',
            name='division',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='General.Division'),
        ),
    ]
