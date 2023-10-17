from rest_framework import status, generics,authentication,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login

from user import models
from user.serializers import UserSerializer,RecruiterSerializer,AuthTokenSerializer
from user.models import UserDetails


# Method to singup a recruiter  
class RecruiterSignupView(generics.CreateAPIView):

    serializer_class = RecruiterSerializer
    queryset = UserDetails.objects.all()

    def create(self,request,*args,**kwargs):
        # Overwriting create method of CreateModelMixin to return success message 
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer)
        return Response({'message': 'Your account has been created successfully'},status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        # To hash the password of recruiter
        instance = serializer.save(is_staff=True)
        instance.set_password(instance.password)
        instance.save()
        
           
# Method to signup seeker
class SeekerSignupView(generics.CreateAPIView):

    serializer_class = UserSerializer
    queryset = UserDetails.objects.all()

    def create(self,request,*args,**kwargs):
        # Overwriting create method of CreateModelMixin to return success message 
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer)
        return Response({'message': 'Your account has been created successfully'},status=status.HTTP_201_CREATED) 

    def perform_create(self, serializer):
        # To hash the password of seeker

        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


# Method to login recruiter and seeker 
class LoginView(APIView):
    
    def post(self,request):
        serializer =AuthTokenSerializer(data = request.data,context={'request':request})
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        token = Token.objects.get(user=user)
        return Response({'token':token.key})    


# Method to view, update and delete a recruiter profile
class RecruiterProfileView(APIView):
    dict ={'detail':'Authentication credentials were not provided.'}  
     
    def get(self,request):
        user = request.user
        
        if request.user.id:
            serializer = RecruiterSerializer(user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(self.dict,status=status.HTTP_401_UNAUTHORIZED)
    
    def patch(self,request): 

        user = request.user
        if user: 
            serializer = RecruiterSerializer(user,data=request.data,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save() 
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(self.dict,status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self,request):

        user = request.user
        if user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(self.dict,status=status.HTTP_401_UNAUTHORIZED)


class SeekerProfileView(APIView):
    dict ={'detail':'Authentication credentials were not provided.'}  

    def get(self,request):

        user = request.user
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response(self.dict,status=status.HTTP_401_UNAUTHORIZED)
    
    def patch(self,request): 

        user = request.user
        if user: 
            serializer = UserSerializer(user,data=request.data,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save() 
            return Response(serializer.data)
        return Response(self.dict,status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self,request):

        user = request.user
        if user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(self.dict,status=status.HTTP_401_UNAUTHORIZED)



# Method to recruiter and seeker logout
class LogoutView(APIView):

    def get(self,request):
        request.user.auth_token.delete()
        return Response({'message':"You've been logged out successfully"})
