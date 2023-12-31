# Generated by Django 4.2.5 on 2023-10-15 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicantDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('job_title', models.CharField(blank=True, max_length=190, null=True)),
                ('company', models.CharField(blank=True, max_length=190, null=True)),
                ('applicant_name', models.CharField(blank=True, max_length=190, null=True)),
                ('applicant_email', models.CharField(blank=True, max_length=190, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('job_title', models.CharField(blank=True, max_length=190, null=True)),
                ('company', models.CharField(blank=True, max_length=190, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('experience', models.CharField(blank=True, max_length=190, null=True)),
                ('work_location', models.CharField(blank=True, max_length=190, null=True)),
                ('employment_type', models.CharField(blank=True, max_length=190, null=True)),
                ('qualification', models.CharField(blank=True, max_length=190, null=True)),
                ('about_company', models.TextField(blank=True, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('openings', models.IntegerField(blank=True, null=True)),
                ('no_of_applicants', models.IntegerField(blank=True, null=True)),
                ('application_deadline', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
