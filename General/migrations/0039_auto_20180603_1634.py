# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-03 11:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('General', '0038_auto_20180603_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentinternship',
            name='internship',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Internship.Internship'),
        ),
        migrations.AlterField(
            model_name='studentinternship',
            name='student',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Registration.Student'),
        ),
    ]
