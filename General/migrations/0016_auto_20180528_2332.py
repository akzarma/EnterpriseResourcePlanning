# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-28 18:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('General', '0015_merge_20180527_1648'),
    ]

    operations = [
        migrations.RenameField(
            model_name='yearsemester',
            old_name='number_of_electives',
            new_name='number_of_electives_groups',
        ),
    ]
