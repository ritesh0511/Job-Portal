# Generated by Django 4.2.5 on 2023-10-15 13:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobdetails',
            name='recruiter_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='applicantdetails',
            name='applicant_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='applicantdetails',
            name='job_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicant', to='job.jobdetails'),
        ),
    ]
