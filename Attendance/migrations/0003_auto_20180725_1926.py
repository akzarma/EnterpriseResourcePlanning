# Generated by Django 2.0.6 on 2018-07-25 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('General', '0002_collegeyear_is_active'),
        ('Attendance', '0002_auto_20180723_1919'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SubjectLectures',
            new_name='SubjectLecture',
        ),
    ]
