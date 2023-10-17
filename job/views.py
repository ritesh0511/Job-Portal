from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework import generics,authentication,permissions,status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from job.serializers import JobSerializer,AplicantSerializer
from job.models import JobDetails,ApplicantDetails
from user.models import UserDetails
from user.serializers import UserSerializer



# Method to create post only accesible to recruiter
class PostJobView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):

        user = request.user
        
        # checking if user is recruiter or not
        if user.is_staff: 
            serializer = JobSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)                                            # checking if user is recruiter or not
            serializer.save(recruiter_id=user,company=user.company,website=user.website,about_company=user.about_company,no_of_applicants=0)                         # passing user instance to JobDetails model - foreignkey
            message = {'message':'job details have been posted successfully'}
            return Response(message,status=status.HTTP_201_CREATED)
        return Response({'message':'You need recruiter privileges to perform this action'},status=status.HTTP_403_FORBIDDEN)
         

# Method to view the recruiter job posts, accessible to only recruiter
class MyPostsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request):
        
        user = request.user

        # checking if user is recruiter or not
        if user.is_staff:
            try:  
                posts = JobDetails.objects.filter(recruiter_id=user.id)                                             
            except JobDetails.DoesNotExist:
                return Response({'detail':'Not found.'})
            serializer =JobSerializer(posts,many=True)                          
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({'message':'You need recruiter privileges to perform this action'},status=status.HTTP_403_FORBIDDEN)
    

# Method to view the job status of provided job_id, only accessible to recruiter
class JobStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]
     
    def get(self,request,job_id):

        user = request.user
        if user.is_staff:
            # retrieving all applicants who had applied for job(job_id)
            applicant = ApplicantDetails.objects.filter(job_id__recruiter_id__id=user.id,job_id=job_id)
            if applicant:
                serializer = AplicantSerializer(applicant,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({'message':'You do not have permission to perform this action'},status=status.HTTP_403_FORBIDDEN)
        return Response({'message':'You need recruiter privileges to perform this action'},status=status.HTTP_403_FORBIDDEN)
            

# Method to view seeker profile only accessible to recruiter
class ViewProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,applicant_id):
     
        user = request.user

        if user.is_staff:
            user = UserDetails.objects.get(id=applicant_id)
            serializer =UserSerializer(user)                          
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({'message':'You need recruiter privileges to perform this action'},status=status.HTTP_403_FORBIDDEN)
    


# Method to update and delete a job, only accessible to recruiter
class JobUpdateDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self,request,pk): 

        user = request.user
        # checking if user is recruiter or not
        if user.is_staff:

            try:                       
                post = JobDetails.objects.get(id=pk)  
            except JobDetails.DoesNotExist: 
                return Response({'detail':'Not found.'},status=status.HTTP_404_NOT_FOUND)
            
            if post.recruiter_id.id == user.id:
                serializer = JobSerializer(post,data=request.data,partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'message':'job details have been updated successfully'},status=status.HTTP_200_OK)
        
            else:
                return Response({'message':'You do not have permission to perform this action'},status=status.HTTP_403_FORBIDDEN)  
        return Response({'message':'You need recruiter privileges to perform this action'},status=status.HTTP_403_FORBIDDEN)
        
    
    def delete(self,request,pk):

        user = request.user

        # checking if user is recruiter or not
        if user.is_staff:

            try:                               
                post = JobDetails.objects.get(id=pk)  
            except JobDetails.DoesNotExist: 
                return Response({'detail':'Not found.'},status=status.HTTP_404_NOT_FOUND)
            
            if post.recruiter_id.id == user.id:
                post.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message':'You do not have permission to perform this action'},status=status.HTTP_403_FORBIDDEN)       
        return Response({'message':'You need recruiter privileges to perform this action'},status=status.HTTP_403_FORBIDDEN)



# Method to list all the jobs
class JobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    queryset = JobDetails.objects.all()



# Method to filter jobs base on searched field
class JobFiltersView(generics.ListAPIView):
    queryset = JobDetails.objects.all()
    serializer_class = JobSerializer
    filter_backends = [SearchFilter]
    search_fields = ['job_title','work_location','company','description']

# Method to apply for a job
class JobApplyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):

        user = request.user
        
        # checking if user is seeker or not
        if not user.is_staff:
            # checking user is applied to job or not
            try:
                applicant = ApplicantDetails.objects.get(applicant_id=user.id,job_id=request.data['job_id'])
            except ApplicantDetails.DoesNotExist:  
                serializer = AplicantSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                job = JobDetails.objects.get(id=request.data['job_id'])      
                serializer.save(job_id=job,job_title=job.job_title,company=job.company,applicant_id=user,applicant_name=user.name,applicant_email=user.email) 
                
                # Incrementing 'no_of_applicants' field after successfully applying a job
                JobDetails.objects.filter(id=request.data['job_id']).update(no_of_applicants=job.no_of_applicants+1)
                message = {'message':'You have successfully applied for this job'}
                return Response(message,status=status.HTTP_200_OK)
            else:
                return Response({'message':'You have already applied for this job'},status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({'message':'You need seeker privileges to perform this action'},status=status.HTTP_403_FORBIDDEN)
    


# Method to view seeker applied jobs,only accessible to seeker
class JobAppliedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
       
        user = request.user
        if not user.is_staff: 
            try:  
                jobs = ApplicantDetails.objects.filter(applicant_id=user.id)                                             # checking if user is recruiter or not
            except ApplicantDetails.DoesNotExist:
                return Response({'detail':'Not found.'})
            serializer =AplicantSerializer(jobs,many=True)           
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({'message':'You need seeker privileges to perform this action'},status=status.HTTP_403_FORBIDDEN)
    

    