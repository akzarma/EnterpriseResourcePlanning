# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-15 15:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Registration', '0022_auto_20180214_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='key',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
