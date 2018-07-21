# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-21 06:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Backup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.FloatField(unique=True)),
                ('date', models.DateTimeField()),
                ('is_latest', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='CurrentDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('current_version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BackupRestore.Backup')),
            ],
        ),
    ]
