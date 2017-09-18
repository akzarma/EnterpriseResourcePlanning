# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-18 14:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('General', '0003_auto_20170918_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branchsubject',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.Branch'),
        ),
        migrations.AlterField(
            model_name='branchsubject',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.Subject'),
        ),
        migrations.AlterField(
            model_name='collegeextradetail',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.Branch'),
        ),
        migrations.AlterField(
            model_name='facultysubject',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.Faculty'),
        ),
        migrations.AlterField(
            model_name='facultysubject',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.Subject'),
        ),
        migrations.AlterField(
            model_name='studentdivision',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.Student'),
        ),
        migrations.AlterField(
            model_name='studentsubject',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.Student'),
        ),
        migrations.AlterField(
            model_name='studentsubject',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.Subject'),
        ),
    ]
