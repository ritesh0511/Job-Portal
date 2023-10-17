from rest_framework import serializers

from job.models import JobDetails,ApplicantDetails

class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobDetails
        exclude = ['recruiter_id']

    def create(self,validated_data):
        return JobDetails.objects.create(**validated_data)


class AplicantSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicantDetails
        # fields = '__all__'
        exclude = ['id']
        read_only_fields = ['job_title','company','applicant_id','applicant_name','applicant_email']

    def create(self,validated_data):
        return ApplicantDetails.objects.create(**validated_data)
