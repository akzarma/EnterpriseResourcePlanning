# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-25 22:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0005_merge_20180426_0350'),
    ]

    operations = [
        migrations.AddField(
            model_name='specificnotification',
            name='type',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='specificnotification',
            name='heading',
            field=models.CharField(max_length=100),
        ),
    ]