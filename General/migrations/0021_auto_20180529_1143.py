# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-29 06:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('General', '0020_auto_20180529_1136'),
    ]

    operations = [
        migrations.RenameField(
            model_name='yearsemester',
            old_name='number_of_electives_groups',
            new_name='number_of_elective_groups',
        ),
    ]
