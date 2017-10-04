# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-18 14:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('Timetable', '0002_auto_20170918_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.Branch'),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.Faculty'),
        ),
    ]