# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-18 16:23
from __future__ import unicode_literals

import Research.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Research', '0010_auto_20171018_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='files',
            field=models.FileField(blank=True, null=True, upload_to=Research.models.faculty_directory_path),
        ),
    ]
