# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 17:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Research', '0013_auto_20170925_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='faculty',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Registration.Faculty'),
        ),
    ]
