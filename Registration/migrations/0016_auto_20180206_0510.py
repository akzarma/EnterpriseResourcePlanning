# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-06 05:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('Registration', '0015_merge_20180123_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='code',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
