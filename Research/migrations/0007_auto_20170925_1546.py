# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 15:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Research', '0006_paper_list_of_files'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paper',
            old_name='list_of_files',
            new_name='files',
        ),
    ]