# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 13:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Research', '0002_paper_faculty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paper',
            name='faculty',
        ),
    ]
