# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-02 12:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('General', '0033_auto_20180602_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='electivebatch',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='electivedivision',
            name='division',
            field=models.IntegerField(default=1),
        ),
    ]
