# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-30 17:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Research', '0014_auto_20170925_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='publication_year',
            field=models.PositiveIntegerField(default=2017),
        ),
    ]
