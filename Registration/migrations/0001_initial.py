# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-19 18:50
from __future__ import unicode_literals

import Registration.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('DOB', models.DateField(default='11/02/1976')),
                ('faculty_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('salary', models.IntegerField(default=10)),
                ('teaching_from', models.DateField(default=datetime.datetime.now)),
                ('subjects_experience', models.CharField(max_length=250)),
                ('projects', models.TextField(blank=True, max_length=300, null=True)),
                ('caste_type', models.CharField(max_length=20)),
                ('mobile', models.BigIntegerField(default=0)),
                ('religion', models.CharField(max_length=20)),
                ('sub_caste', models.CharField(max_length=30)),
                ('handicapped', models.BooleanField(default=0)),
                ('nationality', models.CharField(max_length=50)),
                ('emergency_name', models.CharField(blank=True, max_length=50, null=True)),
                ('emergency_mobile', models.BigIntegerField(blank=True, null=True)),
                ('emergency_relation', models.CharField(blank=True, max_length=50, null=True)),
                ('emergency_address', models.CharField(blank=True, max_length=100, null=True)),
                ('father_name', models.CharField(blank=True, max_length=50, null=True)),
                ('father_profession', models.CharField(blank=True, max_length=30, null=True)),
                ('father_designation', models.CharField(blank=True, max_length=30, null=True)),
                ('father_mobile', models.BigIntegerField(blank=True, null=True)),
                ('father_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('mother_name', models.CharField(blank=True, max_length=50, null=True)),
                ('mother_profession', models.CharField(blank=True, max_length=30, null=True)),
                ('mother_designation', models.CharField(blank=True, max_length=30, null=True)),
                ('mother_mobile', models.BigIntegerField(blank=True, null=True)),
                ('mother_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('permanent_address', models.CharField(blank=True, max_length=100, null=True)),
                ('permanent_state', models.CharField(blank=True, max_length=50, null=True)),
                ('permanent_city', models.CharField(blank=True, max_length=50, null=True)),
                ('permanent_pin_code', models.PositiveIntegerField(blank=True, null=True)),
                ('permanent_country', models.CharField(blank=True, max_length=50, null=True)),
                ('current_address', models.CharField(blank=True, max_length=100, null=True)),
                ('current_state', models.CharField(blank=True, max_length=50, null=True)),
                ('current_city', models.CharField(blank=True, max_length=50, null=True)),
                ('current_pin_code', models.PositiveIntegerField(blank=True, null=True)),
                ('current_country', models.CharField(blank=True, max_length=50, null=True)),
                ('doc', models.FileField(blank=True, null=True, upload_to=Registration.models.faculty_directory_path)),
                ('doc_profile_pic', models.FileField(blank=True, null=True, upload_to=Registration.models.faculty_directory_path)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HOD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField()),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.Branch')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.Faculty')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('DOB', models.DateField(default='1996-02-11')),
                ('admission_type', models.CharField(max_length=50)),
                ('shift', models.CharField(max_length=1)),
                ('caste_type', models.CharField(max_length=20)),
                ('branch', models.CharField(max_length=50)),
                ('gr_number', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('programme', models.CharField(max_length=10)),
                ('mobile', models.BigIntegerField(default=0)),
                ('religion', models.CharField(blank=True, max_length=20, null=True)),
                ('sub_caste', models.CharField(blank=True, max_length=30, null=True)),
                ('handicapped', models.BooleanField(default=0)),
                ('nationality', models.CharField(blank=True, max_length=50, null=True)),
                ('father_name', models.CharField(blank=True, max_length=50, null=True)),
                ('father_profession', models.CharField(blank=True, max_length=30, null=True)),
                ('father_designation', models.CharField(blank=True, max_length=30, null=True)),
                ('father_mobile', models.BigIntegerField(blank=True, default=0, null=True)),
                ('father_email', models.EmailField(blank=True, max_length=100, null=True)),
                ('mother_name', models.CharField(blank=True, max_length=50, null=True)),
                ('mother_profession', models.CharField(blank=True, max_length=30, null=True)),
                ('mother_designation', models.CharField(blank=True, max_length=30, null=True)),
                ('mother_mobile', models.BigIntegerField(blank=True, default=0, null=True)),
                ('mother_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('emergency_name', models.CharField(blank=True, max_length=50, null=True)),
                ('emergency_mobile', models.BigIntegerField(blank=True, null=True)),
                ('emergency_relation', models.CharField(blank=True, max_length=50, null=True)),
                ('emergency_address', models.CharField(blank=True, max_length=100, null=True)),
                ('permanent_address', models.CharField(blank=True, max_length=100, null=True)),
                ('permanent_state', models.CharField(blank=True, max_length=50, null=True)),
                ('permanent_city', models.CharField(blank=True, max_length=50, null=True)),
                ('permanent_pin_code', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
                ('permanent_country', models.CharField(blank=True, max_length=50, null=True)),
                ('current_address', models.CharField(blank=True, max_length=100, null=True)),
                ('current_state', models.CharField(blank=True, max_length=50, null=True)),
                ('current_city', models.CharField(blank=True, max_length=50, null=True)),
                ('current_pin_code', models.IntegerField(blank=True, null=True)),
                ('current_country', models.CharField(blank=True, max_length=50, null=True)),
                ('jee_physics', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('jee_maths', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('jee_chemistry', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('jee_total', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('jee_max_physics', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('jee_max_maths', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('jee_max_chemistry', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('doc_tenth_marksheet', models.FileField(blank=True, null=True, upload_to=Registration.models.student_directory_path)),
                ('doc_twelfth_marksheet', models.FileField(blank=True, null=True, upload_to=Registration.models.student_directory_path)),
                ('doc_jee_marksheet', models.FileField(blank=True, null=True, upload_to=Registration.models.student_directory_path)),
                ('doc_profile_pic', models.ImageField(blank=True, null=True, upload_to=Registration.models.student_directory_path)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('code', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('short_form', models.CharField(max_length=10)),
            ],
        ),
    ]
