# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-05 07:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('Registration', '0003_auto_20171005_0641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='first_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='last_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(max_length=100),
        ),
    ]
