# Generated by Django 2.0.6 on 2018-06-25 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Attendance', '0001_initial'),
        ('Registration', '0001_initial'),
        ('Timetable', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentattendance',
            name='timetable',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Timetable.DateTimetable'),
        ),
        migrations.AddField(
            model_name='facultyattendance',
            name='faculty',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Registration.Faculty'),
        ),
    ]
