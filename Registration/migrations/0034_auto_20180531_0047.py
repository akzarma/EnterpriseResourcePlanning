# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-30 19:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Registration', '0033_remove_subject_elective_group'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='is_elective',
            new_name='is_elective_group',
        ),
    ]
