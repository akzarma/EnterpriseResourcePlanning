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
            name='ExamDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_start_date', models.DateField()),
                ('schedule_end_date', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExamGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExamGroupDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Exam.ExamDetail')),
                ('exam_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Exam.ExamGroup')),
            ],
        ),
        migrations.CreateModel(
            name='ExamGroupRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('exam_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Exam.ExamGroup')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Timetable.Room')),
            ],
        ),
        migrations.CreateModel(
            name='ExamMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_name', models.CharField(max_length=300)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExamSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_datetime', models.DateTimeField(null=True)),
                ('end_datetime', models.DateTimeField(null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('coordinator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.Faculty')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Exam.ExamDetail')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.Subject')),
            ],
        ),
        migrations.CreateModel(
            name='ExamSubjectRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Exam.ExamSubject')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Timetable.Room')),
            ],
        ),
        migrations.CreateModel(
            name='ExamSubjectStudentRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_subject_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Exam.ExamSubjectRoom')),
                ('student_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='General.StudentSubject')),
            ],
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_total', models.IntegerField()),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Exam.ExamDetail')),
                ('student_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='General.StudentSubject')),
            ],
        ),
        migrations.CreateModel(
            name='MarksType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_marks', models.CharField(max_length=200)),
                ('marks_obtained', models.IntegerField()),
                ('max_marks', models.PositiveIntegerField()),
                ('cut_off_marks', models.IntegerField(default=0)),
                ('marks', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Exam.Mark')),
            ],
        ),
        migrations.AddField(
            model_name='examdetail',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Exam.ExamMaster'),
        ),
        migrations.AddField(
            model_name='examdetail',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='General.Semester'),
        ),
        migrations.AddField(
            model_name='examdetail',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='General.YearBranch'),
        ),
    ]
