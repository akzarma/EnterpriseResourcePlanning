# Generated by Django 2.0.6 on 2018-07-20 12:43

import Research.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Registration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField(default=2018)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('type', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=200)),
                ('medium', models.CharField(max_length=50)),
                ('conference_attended', models.BooleanField(default=False)),
                ('level', models.CharField(max_length=50)),
                ('medium_name', models.CharField(max_length=200)),
                ('distribution', models.CharField(max_length=50)),
                ('peer_reviewed', models.BooleanField()),
                ('isbn', models.CharField(max_length=25)),
                ('impact_factor', models.FloatField()),
                ('volume', models.CharField(max_length=20)),
                ('domain', models.CharField(max_length=100)),
                ('paper_with', models.CharField(max_length=20)),
                ('first_author', models.BooleanField()),
                ('funds_from_college', models.PositiveIntegerField()),
                ('other_info', models.CharField(max_length=200)),
                ('files', models.FileField(blank=True, null=True, upload_to=Research.models.faculty_directory_path)),
                ('faculty', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Registration.Faculty')),
            ],
        ),
    ]
