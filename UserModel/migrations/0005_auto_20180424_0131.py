# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-23 20:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserModel', '0004_auto_20180424_0130'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rolemanager',
            old_name='role_obj',
            new_name='role',
        ),
        migrations.RenameField(
            model_name='rolemaster',
            old_name='role_name',
            new_name='role',
        ),
    ]
