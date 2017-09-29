# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 14:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Registration', '0010_auto_20170922_1857'),
        ('Research', '0003_remove_paper_faculty'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='faculty',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to='Registration.Faculty'),
            preserve_default=False,
        ),
    ]
