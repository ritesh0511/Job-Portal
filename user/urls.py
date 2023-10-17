from django.urls import path

from user.views import RecruiterSignupView,SeekerSignupView,LoginView,RecruiterProfileView,SeekerProfileView,LogoutView


urlpatterns = [
    path('recruiter/signup/',RecruiterSignupView.as_view(),name='recruiter-signup'),
    path('seeker/signup/',SeekerSignupView.as_view(),name='seeker-signup'),
    path('login/',LoginView.as_view(),name='login'),
    path('recruiterprofile/',RecruiterProfileView.as_view(),name='recruiter-profile'),
    path('seekerprofile/',SeekerProfileView.as_view(),name='seeker-profile'),
    path('logout/',LogoutView.as_view(),name='logout'),
]