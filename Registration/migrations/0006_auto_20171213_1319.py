# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-13 13:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Registration', '0005_faculty_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]