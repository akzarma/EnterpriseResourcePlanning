# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-15 10:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('Registration', '0025_subject_credits'),
        ('Timetable', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacultyAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_time', models.TimeField()),
                ('out_time', models.TimeField()),
                ('faculty',
                 models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Registration.Faculty')),
            ],
        ),
        migrations.CreateModel(
            name='StudentAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attended', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.Student')),
                ('timetable', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                                to='Timetable.DateTimetable')),
            ],
        ),
        migrations.CreateModel(
            name='TotalAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_lectures', models.PositiveIntegerField()),
                ('attended_lectures', models.PositiveIntegerField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.Student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.Subject')),
            ],
        ),
    ]
