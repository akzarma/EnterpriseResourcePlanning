# Generated by Django 2.0.6 on 2018-07-20 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Timetable', '0001_initial'),
        ('General', '0001_initial'),
        ('Registration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacultyAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_time', models.TimeField()),
                ('out_time', models.TimeField()),
                ('faculty', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Registration.Faculty')),
            ],
        ),
        migrations.CreateModel(
            name='StudentAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attended', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.Student')),
                ('timetable', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Timetable.DateTimetable')),
            ],
        ),
        migrations.CreateModel(
            name='StudentSubjectTotalAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attended', models.IntegerField(default=0)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.Student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.Subject')),
            ],
        ),
        migrations.CreateModel(
            name='SubjectLectures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conducted_lectures', models.IntegerField(default=0)),
                ('faculty_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='General.FacultySubject')),
            ],
        ),
    ]
