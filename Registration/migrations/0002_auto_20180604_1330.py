# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-04 08:00
from __future__ import unicode_literals

import Registration.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Registration', '0001_initial'),
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
        migrations.DeleteModel(
            name='HOD',
        ),
        migrations.AddField(
            model_name='faculty',
            name='DOB',
            field=models.DateField(blank=True, default='1996-02-11', null=True),
        ),
        migrations.AddField(
            model_name='faculty',
            name='first_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='faculty',
            name='last_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='faculty',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='student',
            name='first_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='key',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='last_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subject',
            name='course_pattern',
            field=models.IntegerField(blank=True, default=2015),
        ),
        migrations.AddField(
            model_name='subject',
            name='credits',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='subject',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='is_elective_group',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='doc_profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=Registration.models.faculty_directory_path),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='faculty_code',
            field=models.CharField(max_length=15, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='subject',
            name='code',
            field=models.CharField(blank=True, max_length=20, primary_key=True, serialize=False),
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
