# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-05 07:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Registration', '0004_auto_20171005_0702'),
        ('General', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=10)),
                ('lab', models.BooleanField()),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starting_time', models.IntegerField()),
                ('ending_time', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=10)),
                ('batch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='General.Batch')),
                ('branch_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='General.BranchSubject')),
                ('division', models.ForeignKey(max_length=10, on_delete=django.db.models.deletion.CASCADE, to='General.CollegeExtraDetail')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.Faculty')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Timetable.Room')),
                ('time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Timetable.Time')),
            ],
        ),
    ]
