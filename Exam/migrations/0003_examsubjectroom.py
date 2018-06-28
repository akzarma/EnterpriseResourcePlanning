# Generated by Django 2.0.6 on 2018-06-26 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Timetable', '0003_datetimetable_is_active'),
        ('Exam', '0002_auto_20180625_2241'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamSubjectRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Exam.ExamSubject')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Timetable.Room')),
            ],
        ),
    ]
