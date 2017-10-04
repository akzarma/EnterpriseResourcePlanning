# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 12:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publication_year', models.PositiveIntegerField()),
                ('publication_date', models.DateField(default=datetime.datetime.now)),
                ('type', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=150)),
                ('conference_name', models.CharField(max_length=150)),
                ('conference_type', models.CharField(max_length=20)),
                ('peer_reviewed', models.CharField(max_length=10)),
                ('publication_medium', models.CharField(max_length=10)),
                ('isbn', models.PositiveIntegerField()),
                ('domain', models.CharField(max_length=100)),
                ('funds_received_from_college', models.PositiveIntegerField()),
                ('other_info', models.CharField(max_length=1000)),
            ],
        ),
    ]