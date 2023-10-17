from django.contrib import admin

from job.models import JobDetails,ApplicantDetails

# Register your models here.
admin.site.register(JobDetails)
admin.site.register(ApplicantDetails)
