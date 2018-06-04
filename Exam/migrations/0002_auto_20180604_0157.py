# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-03 20:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Registration', '0032_auto_20180604_0135'),
        ('General', '0001_initial'),
        ('Exam', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='examdetail',
            name='exam',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Exam.ExamMaster'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='examdetail',
            name='semester',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='General.Semester'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='examdetail',
            name='year',
            field=models.ForeignKey(default=13, on_delete=django.db.models.deletion.CASCADE, to='General.YearBranch'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='examsubject',
            name='coordinator',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='Registration.Faculty'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='examsubject',
            name='exam',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Exam.ExamDetail'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='examsubject',
            name='subject',
            field=models.ForeignKey(default=28, on_delete=django.db.models.deletion.CASCADE, to='Registration.Subject'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mark',
            name='student_subject',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='General.StudentSubject'),
            preserve_default=False,
        ),
    ]
