# Generated by Django 2.0.6 on 2018-07-17 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Timetable', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
