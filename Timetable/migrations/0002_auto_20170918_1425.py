# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-18 14:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('Registration', '0002_branch'),
        ('Timetable', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Registration.Branch'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='faculty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Registration.Faculty'),
        ),
    ]