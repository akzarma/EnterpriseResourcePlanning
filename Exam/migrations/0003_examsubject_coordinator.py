# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-28 20:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Registration', '0029_auto_20180527_1451'),
        ('Exam', '0002_auto_20180527_0559'),
    ]

    operations = [
        migrations.AddField(
            model_name='examsubject',
            name='coordinator',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='Registration.Faculty'),
            preserve_default=False,
        ),
    ]
