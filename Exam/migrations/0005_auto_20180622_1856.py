# Generated by Django 2.0.6 on 2018-06-22 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Exam', '0004_examgroup_examgroupdetail_examgrouproom'),
    ]

    operations = [
        migrations.AddField(
            model_name='examsubject',
            name='end_datetime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='examsubject',
            name='start_datetime',
            field=models.DateTimeField(null=True),
        ),
    ]