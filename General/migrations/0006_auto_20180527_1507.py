# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-27 09:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('General', '0005_auto_20180527_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentdetail',
            name='batch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='General.Batch'),
        ),
    ]