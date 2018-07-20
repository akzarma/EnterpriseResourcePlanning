# Generated by Django 2.0.6 on 2018-07-07 23:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('General', '0001_initial'),
        ('Registration', '0002_auto_20180708_0511'),
        ('Attendance', '0001_initial'),
    ]

    operations = [
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
        migrations.RemoveField(
            model_name='totalattendance',
            name='student',
        ),
        migrations.RemoveField(
            model_name='totalattendance',
            name='subject',
        ),
        migrations.AddField(
            model_name='studentattendance',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.DeleteModel(
            name='TotalAttendance',
        ),
    ]
