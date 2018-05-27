# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-26 22:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Exam', '0002_examdetail_exam'),
        ('Registration', '0028_auto_20180426_0036'),
        ('General', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='examdetail',
            name='semester',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='General.Semester'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='examdetail',
            name='year',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='General.YearBranch'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='examsubject',
            name='exam',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='Exam.ExamDetail'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='examsubject',
            name='subject',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='Registration.Subject'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mark',
            name='student_subject',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='General.StudentSubject'),
            preserve_default=False,
        ),
    ]
