# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-23 21:53
from __future__ import unicode_literals

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
            name='RoleManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end_date', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoleMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=200)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='rolemanager',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserModel.RoleMaster'),
        ),
        migrations.AddField(
            model_name='rolemanager',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
