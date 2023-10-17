from django.db import models

# Create your models here.


class JobDetails(models.Model):
    id = models.AutoField(primary_key=True)
    job_title = models.CharField(max_length=190,null=True,blank=True)
    company = models.CharField(max_length=190,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    experience = models.CharField(max_length=190,null=True,blank=True)
    work_location = models.CharField(max_length=190,null=True,blank=True)
    employment_type = models.CharField(max_length=190,null=True,blank=True)
    qualification = models.CharField(max_length=190,null=True,blank=True)
    about_company = models.TextField(null=True,blank=True)
    website = models.URLField(null=True,blank=True)
    openings = models.IntegerField(null=True,blank=True)
    no_of_applicants = models.IntegerField(null=True,blank=True)
    application_deadline = models.DateField(null=True,blank=True)
    recruiter_id = models.ForeignKey('user.UserDetails',on_delete=models.CASCADE) 



class ApplicantDetails(models.Model):
    id = models.AutoField(primary_key=True)
    job_id = models.ForeignKey('JobDetails',on_delete=models.CASCADE,related_name='applicant')
    job_title = models.CharField(max_length=190,null=True,blank=True)
    company = models.CharField(max_length=190,null=True,blank=True)
    applicant_id = models.ForeignKey('user.UserDetails',on_delete=models.CASCADE)
    applicant_name = models.CharField(max_length=190,null=True,blank=True)
    applicant_email = models.CharField(max_length=190,null=True,blank=True)