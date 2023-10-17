from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework.utils import json

# Create your tests here.

def create_admin(**params):
    return get_user_model().objects.create_admin(**params)

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class TestCase(APITestCase):
    maxDiff = None
    
    def setUp(self) -> None:
        self.client = APIClient()


    def test_recruiter_signup(self):
        payload = {'name':'recruiter','designation':'HR','company':'ABC Tech Solutions','email':'recruiter@xyz.com',
                   'date_of_birth':'1989-02-03','gender':'Male','mobile_number':9123456789,
                   'about_company':'ABC Tech Solutions was established in 1996 to provides technology and consulting services',
                   'website':'http://www.abctech.com/','password':'Pass@123'}
        response = self.client.post('/recruiter/signup/', data=payload, format='json') 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content,{'message':'Your account has been created successfully'})

        payload = {'name':'testrecruiter2','designation':'HR','company':'XYZ Tech Solutions','email':'testrecruiter2@xyz.com',
                   'date_of_birth':'1967-12-23','gender':'Male','mobile_number':9111111111,
                   'about_company':'XYZ Tech Solutions was established in 1969 to provides technology and consulting services',
                   'website':'http://www.xyztech.com/','password':'Pass@123'}
        response = self.client.post('/recruiter/signup/', data=payload, format='json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content,{'name':['Enter a valid name']})
        
        payload = {'name':'testrecruiter','designation':'HR','company':'ABC Tech Solutions','email':'recruiter@.com',
                   'date_of_birth':'1989-02-03','gender':'Male','mobile_number':9111111111,
                   'about_company':'ABC Tech Solutions was established in 1996 to provides technology and consulting services',
                   'website':'http://www.abctech.com/','password':'Pass@123'}
        response = self.client.post('/recruiter/signup/', data=payload, format='json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content,{'email':['Enter a valid email']})

        payload = {'name':'testrecruiter','designation':'HR','company':'ABC Tech Solutions','email':'recruiter@xyz.com',
                   'date_of_birth':'1989-02-03','gender':'Male','mobile_number':9111111111,
                   'about_company':'ABC Tech Solutions was established in 1996 to provides technology and consulting services',
                   'website':'http://www.abctech.com/','password':'Pass@123'}
        response = self.client.post('/recruiter/signup/', data=payload, format='json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content,{'email':['user details with this email already exists.']})

        payload = {'name':'testrecruiter','designation':'HR','company':'ABC Tech Solutions','email':'testrecruiter@xyz.com',
                   'date_of_birth':'1989-02-03','gender':'Male','mobile_number':91234,
                   'about_company':'ABC Tech Solutions was established in 1996 to provides technology and consulting services',
                   'website':'http://www.abctech.com/','password':'Pass@123'}
        response = self.client.post('/recruiter/signup/', data=payload, format='json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content,{'mobile_number':['Enter a valid mobile number']})

        payload = {'name':'testrecruiter','designation':'HR','company':'ABC Tech Solutions','email':'testrecruiter@xyz.com',
                   'date_of_birth':'1989-02-03','gender':'Male','mobile_number':9123456789,
                   'about_company':'ABC Tech Solutions was established in 1996 to provides technology and consulting services',
                   'website':'http://www.abctech.com/','password':'Pass@123'}
        response = self.client.post('/recruiter/signup/', data=payload, format='json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content,{'mobile_number':['user details with this mobile number already exists.']})

        payload = {'name':'testrecruiter','designation':'HR','company':'ABC Tech Solutions','email':'testrecruiter@xyz.com',
                   'date_of_birth':'1989-02-03','gender':'Male','mobile_number':9111111111,
                   'about_company':'ABC Tech Solutions was established in 1996 to provides technology and consulting services',
                   'website':'http://www.abctech.com/','password':'Pass'}
        response = self.client.post('/recruiter/signup/', data=payload, format='json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content,{'password':['Enter a valid password']})

        payload = {'name':'testrecruiter','designation':'HR','company':'ABC Tech Solutions','email':'testrecruiter@xyz.com',
                   'date_of_birth':'1989-02-03','gender':'Male','mobile_number':9111111111,
                   'about_company':'ABC Tech Solutions was established in 1996 to provides technology and consulting services',
                   'website':'http://www.abctech.com/','password':'Pass@123'}
        response = self.client.post('/recruiter/signup/', data=payload, format='json') 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content,{'message':'Your account has been created successfully'})


    def test_seeker_signup(self):
        payload = {'name':'seeker','email':'seeker@abc.com','date_of_birth':'1987-09-08','gender':'Male','mobile_number':8111111111,
                   'address':'Buldhana,Maharashtra','password':'Test@123','course':'BE','specialization':'Mechanical Engineer',
                   'course_type':'Full-time','college':'P R Pote','percentage':'97','year_of_passing':'2020','skills':'Python,Django,HTML,CSS',
                   'summary':'To achieve the objectives of the company with honesty and fairness','experience_level':'Fresher','designation':'System Engineer',
                   'responsibility':'As per requirement','company':'TCS','location':'Pune','worked_from':'2020-09-07','to':'2023-10-01'}
        response = self.client.post('/seeker/signup/',data=payload,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'Your account has been created successfully'})

        payload = {'name':'testseeker65','email':'testseeker@abc.com','date_of_birth':'1987-09-08','gender':'Male','mobile_number':8222222222,
                   'address':'Buldhana,Maharashtra','password':'Test@123','course':'BE','specialization':'Mechanical Engineer',
                   'course_type':'Full-time','college':'P R Pote','percentage':'97','year_of_passing':'2020','skills':'Python,Django,HTML,CSS',
                   'summary':'To achieve the objectives of the company with honesty and fairness','experience_level':'Fresher','designation':'System Engineer',
                   'responsibility':'As per requirement','company':'TCS','location':'Pune','worked_from':'2020-09-07','to':'2023-10-01'}
        response = self.client.post('/seeker/signup/',data=payload,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'name':['Enter a valid name']})

        payload = {'name':'testseeker','email':'testseeker@abc','date_of_birth':'1987-09-08','gender':'Male','mobile_number':8222222222,
                   'address':'Buldhana,Maharashtra','password':'Test@123','course':'BE','specialization':'Mechanical Engineer',
                   'course_type':'Full-time','college':'P R Pote','percentage':'97','year_of_passing':'2020','skills':'Python,Django,HTML,CSS',
                   'summary':'To achieve the objectives of the company with honesty and fairness','experience_level':'Fresher','designation':'System Engineer',
                   'responsibility':'As per requirement','company':'TCS','location':'Pune','worked_from':'2020-09-07','to':'2023-10-01'}
        response = self.client.post('/seeker/signup/',data=payload,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'email':['Enter a valid email']})

        payload = {'name':'testseeker','email':'seeker@abc.com','date_of_birth':'1987-09-08','gender':'Male','mobile_number':8222222222,
                   'address':'Buldhana,Maharashtra','password':'Test@123','course':'BE','specialization':'Mechanical Engineer',
                   'course_type':'Full-time','college':'P R Pote','percentage':'97','year_of_passing':'2020','skills':'Python,Django,HTML,CSS',
                   'summary':'To achieve the objectives of the company with honesty and fairness','experience_level':'Fresher','designation':'System Engineer',
                   'responsibility':'As per requirement','company':'TCS','location':'Pune','worked_from':'2020-09-07','to':'2023-10-01'}
        response = self.client.post('/seeker/signup/',data=payload,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'email':['user details with this email already exists.']})

        payload = {'name':'testseeker','email':'testseeker@abc.com','date_of_birth':'1987-09-08','gender':'Male','mobile_number':822222,
                   'address':'Buldhana,Maharashtra','password':'Test@123','course':'BE','specialization':'Mechanical Engineer',
                   'course_type':'Full-time','college':'P R Pote','percentage':'97','year_of_passing':'2020','skills':'Python,Django,HTML,CSS',
                   'summary':'To achieve the objectives of the company with honesty and fairness','experience_level':'Fresher','designation':'System Engineer',
                   'responsibility':'As per requirement','company':'TCS','location':'Pune','worked_from':'2020-09-07','to':'2023-10-01'}
        response = self.client.post('/seeker/signup/',data=payload,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'mobile_number':['Enter a valid mobile number']})

        payload = {'name':'testseeker','email':'testseeker@abc.com','date_of_birth':'1987-09-08','gender':'Male','mobile_number':8111111111,
                   'address':'Buldhana,Maharashtra','password':'Test@123','course':'BE','specialization':'Mechanical Engineer',
                   'course_type':'Full-time','college':'P R Pote','percentage':'97','year_of_passing':'2020','skills':'Python,Django,HTML,CSS',
                   'summary':'To achieve the objectives of the company with honesty and fairness','experience_level':'Fresher','designation':'System Engineer',
                   'responsibility':'As per requirement','company':'TCS','location':'Pune','worked_from':'2020-09-07','to':'2023-10-01'}
        response = self.client.post('/seeker/signup/',data=payload,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'mobile_number':['user details with this mobile number already exists.']})

        payload = {'name':'testseeker','email':'testseeker@abc.com','date_of_birth':'1987-09-08','gender':'Male','mobile_number':8222222222,
                   'address':'Buldhana,Maharashtra','password':'Test','course':'BE','specialization':'Mechanical Engineer',
                   'course_type':'Full-time','college':'P R Pote','percentage':'97','year_of_passing':'2020','skills':'Python,Django,HTML,CSS',
                   'summary':'To achieve the objectives of the company with honesty and fairness','experience_level':'Fresher','designation':'System Engineer',
                   'responsibility':'As per requirement','company':'TCS','location':'Pune','worked_from':'2020-09-07','to':'2023-10-01'}
        response = self.client.post('/seeker/signup/',data=payload,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'password':['Enter a valid password']})

        payload = {'name':'testseeker','email':'testseeker@abc.com','date_of_birth':'1987-09-08','gender':'Male','mobile_number':8222222222,
                   'address':'Buldhana,Maharashtra','password':'Test@123','course':'BE','specialization':'Mechanical Engineer',
                   'course_type':'Full-time','college':'P R Pote','percentage':'97','year_of_passing':'2020','skills':'Python,Django,HTML,CSS',
                   'summary':'To achieve the objectives of the company with honesty and fairness','experience_level':'Fresher','designation':'System Engineer',
                   'responsibility':'As per requirement','company':'TCS','location':'Pune','worked_from':'2020-09-07','to':'2023-10-01'}
        response = self.client.post('/seeker/signup/',data=payload,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'Your account has been created successfully'})

    # Initialize payloads
    recruiter = {'name':'recruiter','designation':'HR','company':'ABC Tech Solutions','email':'recruiter@xyz.com',
                   'date_of_birth':'1989-02-03','gender':'Male','mobile_number':9123456789,
                   'about_company':'ABC Tech Solutions was established in 1996 to provides technology and consulting services',
                   'website':'http://www.abctech.com/','password':'Pass@123'}
        
    testrecruiter = {'name':'testrecruiter','designation':'HR','company':'ABC Tech Solutions','email':'testrecruiter@xyz.com',
                   'date_of_birth':'1989-02-03','gender':'Male','mobile_number':9111111111,
                   'about_company':'ABC Tech Solutions was established in 1996 to provides technology and consulting services',
                   'website':'http://www.abctech.com/','password':'Pass@123'}
        
    seeker = {'name':'seeker','email':'seeker@abc.com','date_of_birth':'1987-09-08','gender':'Male','mobile_number':8111111111,
                   'address':'Buldhana,Maharashtra','password':'Test@123','course':'BE','specialization':'Mechanical Engineer',
                   'course_type':'Full-time','college':'P R Pote','percentage':'97','year_of_passing':'2020','skills':'Python,Django,HTML,CSS',
                   'summary':'To achieve the objectives of the company with honesty and fairness','experience_level':'Fresher','designation':'System Engineer',
                   'responsibility':'As per requirement','company':'TCS','location':'Pune','worked_from':'2020-09-07','to':'2023-10-01'}
        
    testseeker = {'name':'testseeker','email':'testseeker@abc.com','date_of_birth':'1987-09-08','gender':'Male','mobile_number':8222222222,
                   'address':'Buldhana,Maharashtra','password':'Test@123','course':'BE','specialization':'Mechanical Engineer',
                   'course_type':'Full-time','college':'P R Pote','percentage':'97','year_of_passing':'2020','skills':'Python,Django,HTML,CSS',
                   'summary':'To achieve the objectives of the company with honesty and fairness','experience_level':'Fresher','designation':'System Engineer',
                   'responsibility':'As per requirement','company':'TCS','location':'Pune','worked_from':'2020-09-07','to':'2023-10-01'}
        

    def test_login(self):
        create_admin(**TestCase.testrecruiter)

        create_user(**TestCase.testseeker)

        # login recruiter
        payload = {'email':'testrecruiter@xyz.com','password':'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)

        # login seeker with invalid details
        payload = {'email':'testseeker@abc.com','password':'Test'}
        response = self.client.post('/login/',data=payload, format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content,{"non_field_errors":["Unable to authenticate with provided credentials"]})

        # login seeker
        payload = {'email':'testseeker@abc.com','password':'Test@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('token',response.data)


    def test_access_profile_with_invalid_token(self):
        create_admin(**TestCase.testrecruiter)

        create_user(**TestCase.testseeker)

        payload = {'email':'testrecruiter@xyz.com','password':'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        #try to view profile without token
        self.client.credentials()
        response = self.client.get('/recruiterprofile/')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content,{"detail":"Authentication credentials were not provided."})


        payload = {'email':'testseeker@abc.com','password':'Test@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        # try to view profile with invalid token
        self.client.credentials(HTTP_AUTHORIZATION='Token jlgg')
        response = self.client.get('/seekerprofile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'detail':'Invalid token.'})


    def test_recruiter_profile_view(self):
        create_admin(**TestCase.testrecruiter)

        payload = {'email':'testrecruiter@xyz.com','password':'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        # view profile
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/recruiterprofile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = (response.content.decode('utf-8'))
        self.assertJSONEqual(response_content, {'name':'testrecruiter','designation':'HR','company':'ABC Tech Solutions','email':'testrecruiter@xyz.com',
                   'date_of_birth':'1989-02-03','gender':'Male','mobile_number':9111111111,
                   'about_company':'ABC Tech Solutions was established in 1996 to provides technology and consulting services',
                   'website':'http://www.abctech.com/'})
        
    
    def test_update_recruiter_profile(self):
        create_admin(**TestCase.testrecruiter)

        payload = {'email':'testrecruiter@xyz.com','password':'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        # update profile
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        payload = {'mobile_number':9333333333}
        response = self.client.patch('/recruiterprofile/', data=payload, format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'name':'testrecruiter','designation':'HR','company':'ABC Tech Solutions','email':'testrecruiter@xyz.com',
                   'date_of_birth':'1989-02-03','gender':'Male','mobile_number':9333333333,
                   'about_company':'ABC Tech Solutions was established in 1996 to provides technology and consulting services',
                   'website':'http://www.abctech.com/'})
        

    def test_delete_recruiter_profile(self):
        create_admin(**TestCase.testrecruiter)

        payload = {'email':'testrecruiter@xyz.com','password':'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        # delete profile
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.delete('/recruiterprofile/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

            
    def test_seeker_profile_view(self):
        create_user(**TestCase.testseeker)

        payload = {'email':'testseeker@abc.com','password':'Test@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        # view profile
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/seekerprofile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'name':'testseeker','email':'testseeker@abc.com','date_of_birth':'1987-09-08','gender':'Male','mobile_number':8222222222,
                   'address':'Buldhana,Maharashtra','course':'BE','specialization':'Mechanical Engineer',
                   'course_type':'Full-time','college':'P R Pote','percentage':'97.00','year_of_passing':2020,'skills':'Python,Django,HTML,CSS',
                   'summary':'To achieve the objectives of the company with honesty and fairness','experience_level':'Fresher','designation':'System Engineer',
                   'responsibility':'As per requirement','company':'TCS','location':'Pune','worked_from':'2020-09-07','to':'2023-10-01'}
        )
        
    
    def test_update_seeker_profile(self):
        create_user(**TestCase.testseeker)

        payload = {'email':'testseeker@abc.com','password':'Test@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        # update profile
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        payload = {'mobile_number':8333333333}
        response = self.client.patch('/seekerprofile/', data=payload, format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'name':'testseeker','email':'testseeker@abc.com','date_of_birth':'1987-09-08','gender':'Male','mobile_number':8333333333,
                   'address':'Buldhana,Maharashtra','course':'BE','specialization':'Mechanical Engineer',
                   'course_type':'Full-time','college':'P R Pote','percentage':'97.00','year_of_passing':2020,'skills':'Python,Django,HTML,CSS',
                   'summary':'To achieve the objectives of the company with honesty and fairness','experience_level':'Fresher','designation':'System Engineer',
                   'responsibility':'As per requirement','company':'TCS','location':'Pune','worked_from':'2020-09-07','to':'2023-10-01'}
        )
        

    def test_delete_seeker_profile(self):
        create_user(**TestCase.testseeker)

        payload = {'email':'testseeker@abc.com','password':'Test@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        # delete profile
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.delete('/seekerprofile/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_recruiter_logout(self):
        create_admin(**TestCase.testrecruiter)

        payload = {'email':'testrecruiter@xyz.com','password':'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        # logout
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"message":"You've been logged out successfully"})

        # try to view profile after logout
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/recruiterprofile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"detail":"Invalid token."})

        # try to update profile after logout
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        payload = {'mobile_number':9333333333}
        response = self.client.patch('/recruiterprofile/', data=payload, format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"detail":"Invalid token."})

        # try to delete profile after logout
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.delete('/recruiterprofile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_seeker_logout(self):
        create_admin(**TestCase.testseeker)

        payload = {'email':'testseeker@abc.com','password':'Test@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        # logout
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"message":"You've been logged out successfully"})

        # try to view profile after logout
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/seekerprofile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"detail":"Invalid token."})

        # try to update profile after logout
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        payload = {'mobile_number':8333333333}
        response = self.client.patch('/seekerprofile/', data=payload, format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"detail":"Invalid token."})

        # try to delete profile after logout
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.delete('/seekerprofile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
