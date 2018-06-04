# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-03 20:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Registration', '0031_auto_20180529_0353'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElectiveSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('short_form', models.CharField(max_length=10)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.RenameField(
            model_name='subject',
            old_name='is_elective',
            new_name='is_elective_group',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='elective_group',
        ),
        migrations.AddField(
            model_name='subject',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='short_form',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AddField(
            model_name='electivesubject',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.Subject'),
        ),
    ]
