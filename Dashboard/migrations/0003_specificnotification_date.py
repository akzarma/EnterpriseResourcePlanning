# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-24 16:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0002_auto_20180423_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='specificnotification',
            name='date',
            field=models.DateField(null=True),
        ),
    ]