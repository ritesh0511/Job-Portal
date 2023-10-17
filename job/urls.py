from django.urls import path

from job.views import PostJobView,MyPostsView,ViewProfileView,JobUpdateDeleteView,JobListView,JobFiltersView,JobApplyView,JobAppliedView,JobStatusView

urlpatterns = [
    path('postjob/',PostJobView.as_view()),
    path('myposts/',MyPostsView.as_view()),
    path('listjob/',JobListView.as_view()),
    path('filterjob/',JobFiltersView.as_view()),
    path('applyjob/',JobApplyView.as_view()),
    path('appliedjobs/',JobAppliedView.as_view()),
    path('jobstatus/<int:job_id>/',JobStatusView.as_view()),
    path('viewprofile/<int:applicant_id>/',ViewProfileView.as_view()),
    path('updatejob/<int:pk>/',JobUpdateDeleteView.as_view()),

]