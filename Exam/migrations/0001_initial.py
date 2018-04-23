# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-23 20:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('General', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_start_date', models.DateField()),
                ('schedule_end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='ExamMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_name', models.CharField(max_length=300)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_total', models.IntegerField()),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Exam.ExamDetail')),
                ('student_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='General.StudentSubject')),
            ],
        ),
        migrations.CreateModel(
            name='MarksType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_marks', models.CharField(max_length=200)),
                ('marks_obtained', models.IntegerField()),
                ('max_marks', models.PositiveIntegerField()),
                ('cut_off_marks', models.IntegerField(default=0)),
                ('marks', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Exam.Mark')),
            ],
        ),
        migrations.AddField(
            model_name='examdetail',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Exam.ExamMaster'),
        ),
        migrations.AddField(
            model_name='examdetail',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='General.Semester'),
        ),
        migrations.AddField(
            model_name='examdetail',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='General.Division'),
        ),
    ]
