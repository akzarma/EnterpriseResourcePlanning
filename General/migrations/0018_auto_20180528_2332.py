# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-28 18:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('General', '0017_auto_20180528_2332'),
    ]

    operations = [
        migrations.RenameField(
            model_name='yearsemester',
            old_name='number_of_electives',
            new_name='number_of_electives_groups',
        ),
    ]
