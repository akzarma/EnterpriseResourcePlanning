# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-18 15:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('Registration', '0005_auto_20170918_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='short_form',
            field=models.CharField(max_length=10),
        ),
    ]