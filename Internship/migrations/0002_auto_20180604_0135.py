# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-03 20:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Registration', '0032_auto_20180604_0135'),
        ('Internship', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='internship',
            name='branch',
            field=models.ForeignKey(blank=True, default=0, on_delete=django.db.models.deletion.CASCADE, to='Registration.Branch'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='internship',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
