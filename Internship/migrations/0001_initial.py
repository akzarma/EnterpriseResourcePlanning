# Generated by Django 2.0.6 on 2018-06-28 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Registration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Internship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=300)),
                ('address', models.CharField(max_length=500)),
                ('email', models.EmailField(max_length=254)),
                ('contact_number', models.IntegerField()),
                ('website', models.CharField(max_length=50)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('branch', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Registration.Branch')),
            ],
        ),
    ]
