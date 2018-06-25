# Generated by Django 2.0.6 on 2018-06-25 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Registration', '0001_initial'),
        ('General', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DateTimetable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('not_available', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_substituted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=10)),
                ('lab', models.BooleanField()),
                ('capacity', models.PositiveIntegerField(default=28)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starting_time', models.IntegerField()),
                ('ending_time', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=10)),
                ('is_practical', models.BooleanField(default=False)),
                ('batch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='General.Batch')),
                ('branch_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='General.BranchSubject')),
                ('division', models.ForeignKey(max_length=10, null=True, on_delete=django.db.models.deletion.CASCADE, to='General.Division')),
                ('elective_division', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='General.ElectiveDivision')),
                ('elective_subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Registration.ElectiveSubject')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.Faculty')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Timetable.Room')),
                ('time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Timetable.Time')),
            ],
        ),
        migrations.AddField(
            model_name='datetimetable',
            name='original',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='original', to='Timetable.Timetable'),
        ),
        migrations.AddField(
            model_name='datetimetable',
            name='substitute',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='substitute', to='Timetable.Timetable'),
        ),
    ]
