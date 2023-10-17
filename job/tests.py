from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.utils import json
from django.contrib.auth import get_user_model

# Create your tests here.

def create_admin(**params):
    return get_user_model().objects.create_admin(**params)

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class JobTestCase(APITestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.client = APIClient()
    
    recruiter = {'name':'recruiter','designation':'HR','company':'ABC Tech Solutions','email':'recruiter@xyz.com',
                   'date_of_birth':'1989-02-03','gender':'Male','mobile_number':9111111111,
                   'about_company':'ABC Tech Solutions was established in 1996 to provides technology and consulting services',
                   'website':'http://www.abctech.com/','password':'Pass@123'}
        
    testrecruiter = {'name':'testrecruiter','designation':'HR','company':'ABC Tech Solutions','email':'testrecruiter@xyz.com',
                   'date_of_birth':'1989-02-03','gender':'Male','mobile_number':9222222222,
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

    def test_post_job_without_recruiter_access(self):
        create_user(**JobTestCase.testseeker)

        payload = {'email':'testseeker@abc.com','password':'Test@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title':'Web developer','description':'We are looking for talented web developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','application_deadline':'2020-12-09'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'You need recruiter privileges to perform this action'})


    def test_post_job(self):
        create_admin(**JobTestCase.recruiter)

        create_admin(**JobTestCase.testrecruiter)

        payload = {'email':'recruiter@xyz.com','password':'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title':'Web developer','description':'We are looking for talented web developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','openings':2,'application_deadline':'2020-12-09'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = (response.content.decode('utf-8'))
        self.assertJSONEqual(response_content, {'message':'job details have been posted successfully'})

        payload = {'email':'testrecruiter@xyz.com','password':'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        # try to post job without token
        payload = {'job_title':'Python developer','description':'We are looking for talented python developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','openings':2,'application_deadline':'2020-12-09'}
        self.client.credentials()
        response = self.client.post('/postjob/',data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'detail':'Authentication credentials were not provided.'})

        # try to post job with invalid token
        payload = {'job_title':'Python developer','description':'We are looking for talented web developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','openings':2,'application_deadline':'2020-12-09'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ujeogjfl')
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'detail':'Invalid token.'})

        payload = {'job_title':'Python developer','description':'We are looking for talented web developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','openings':2,'application_deadline':'2020-12-09'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'job details have been posted successfully'})


    def test_myposts_without_recruiter_access(self):
        create_user(**JobTestCase.testseeker)

        payload = {'email':'testseeker@abc.com','password':'Test@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/myposts/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'You need recruiter privileges to perform this action'})


    def test_myposts(self):
        create_admin(**JobTestCase.recruiter)
        maxDiff = None

        payload = {'email':'recruiter@xyz.com','password':'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title':'Web developer','description':'We are looking for talented web developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','openings':2,'application_deadline':'2020-12-09'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'job details have been posted successfully'})

        # myposts
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/myposts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, [{'id':1,'job_title':'Web developer','company':'ABC Tech Solutions','description':'We are looking for talented web developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','about_company':'ABC Tech Solutions was established in 1996 to provides technology and consulting services',
                   'website':'http://www.abctech.com/','no_of_applicants':0,'openings':2,'application_deadline':'2020-12-09'}])
        
    
    def test_list_and_filter_job(self):
        create_admin(**JobTestCase.recruiter)

        create_admin(**JobTestCase.testrecruiter)

        payload = {'email':'recruiter@xyz.com','password':'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title':'Web developer','description':'We are looking for talented web developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','openings':2,'application_deadline':'2020-12-09'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'job details have been posted successfully'})

        payload = {'email':'testrecruiter@xyz.com','password':'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']
        
        payload = {'job_title':'Python developer','description':'We are looking for talented python developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','openings':2,'application_deadline':'2020-12-09'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'job details have been posted successfully'})

        # list job
        response = self.client.get('/listjob/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, [{'id':1,'job_title':'Web developer','company':'ABC Tech Solutions','description':'We are looking for talented web developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','about_company':'ABC Tech Solutions was established in 1996 to provides technology and consulting services',
                   'website':'http://www.abctech.com/','no_of_applicants':0,'openings':2,'application_deadline':'2020-12-09'},
                   {'id':2,'job_title':'Python developer','company':'ABC Tech Solutions','description':'We are looking for talented python developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','about_company':'ABC Tech Solutions was established in 1996 to provides technology and consulting services',
                   'website':'http://www.abctech.com/','no_of_applicants':0,'openings':2,'application_deadline':'2020-12-09'}])
        
        # filter job by title
        response = self.client.get('/filterjob/?search=Web+developer')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, [{'id':1,'job_title':'Web developer','company':'ABC Tech Solutions','description':'We are looking for talented web developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','about_company':'ABC Tech Solutions was established in 1996 to provides technology and consulting services',
                   'website':'http://www.abctech.com/','no_of_applicants':0,'openings':2,'application_deadline':'2020-12-09'},
                   ])
        
        # filter job by location
        response = self.client.get('/filterjob/?search=Pune')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, [{'id':1,'job_title':'Web developer','company':'ABC Tech Solutions','description':'We are looking for talented web developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','about_company':'ABC Tech Solutions was established in 1996 to provides technology and consulting services',
                   'website':'http://www.abctech.com/','no_of_applicants':0,'openings':2,'application_deadline':'2020-12-09'},
                   {'id':2,'job_title':'Python developer','company':'ABC Tech Solutions','description':'We are looking for talented python developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','about_company':'ABC Tech Solutions was established in 1996 to provides technology and consulting services',
                   'website':'http://www.abctech.com/','no_of_applicants':0,'openings':2,'application_deadline':'2020-12-09'}])

        # filter job by skill
        response = self.client.get('/filterjob/?search=Python')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, [{'id':1,'job_title':'Web developer','company':'ABC Tech Solutions','description':'We are looking for talented web developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','about_company':'ABC Tech Solutions was established in 1996 to provides technology and consulting services',
                   'website':'http://www.abctech.com/','no_of_applicants':0,'openings':2,'application_deadline':'2020-12-09'},
                   {'id':2,'job_title':'Python developer','company':'ABC Tech Solutions','description':'We are looking for talented python developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','about_company':'ABC Tech Solutions was established in 1996 to provides technology and consulting services',
                   'website':'http://www.abctech.com/','no_of_applicants':0,'openings':2,'application_deadline':'2020-12-09'}])

        # filter job by company
        response = self.client.get('/filterjob/?search=ABC+Tech+Solutions')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, [{'id':1,'job_title':'Web developer','company':'ABC Tech Solutions','description':'We are looking for talented web developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','about_company':'ABC Tech Solutions was established in 1996 to provides technology and consulting services',
                   'website':'http://www.abctech.com/','no_of_applicants':0,'openings':2,'application_deadline':'2020-12-09'},
                   {'id':2,'job_title':'Python developer','company':'ABC Tech Solutions','description':'We are looking for talented python developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','about_company':'ABC Tech Solutions was established in 1996 to provides technology and consulting services',
                   'website':'http://www.abctech.com/','no_of_applicants':0,'openings':2,'application_deadline':'2020-12-09'}])

    
    def test_apply_job(self):
        create_admin(**JobTestCase.recruiter)

        create_admin(**JobTestCase.testrecruiter)

        create_user(**JobTestCase.seeker)

        create_user(**JobTestCase.testseeker)

        payload = {'email':'recruiter@xyz.com','password':'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title':'Web developer','description':'We are looking for talented web developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','openings':1,'application_deadline':'2020-12-09'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = (response.content.decode('utf-8'))
        self.assertJSONEqual(response_content, {'message':'job details have been posted successfully'})

        payload = {'email':'testrecruiter@xyz.com','password':'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']
        
        payload = {'job_title':'Python developer','description':'We are looking for talented python developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','openings':2,'application_deadline':'2020-12-09'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'job details have been posted successfully'})

        # recruiter try to apply job
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        payload = {'job_id':1}
        response = self.client.post('/applyjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'You need seeker privileges to perform this action'})

        payload = {'email':'seeker@abc.com','password':'Test@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']        

        # try to apply job without token
        self.client.credentials()
        payload = {'job_id':1}
        response = self.client.post('/applyjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'detail':'Authentication credentials were not provided.'})

        # try to apply job with invalid token
        self.client.credentials(HTTP_AUTHORIZATION='Token gjajs')
        payload = {'job_id':1}
        response = self.client.post('/applyjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'detail':'Invalid token.'})

        # apply job
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        payload = {'job_id':1}
        response = self.client.post('/applyjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'You have successfully applied for this job'})

        # try to apply same job again
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        payload = {'job_id':1}
        response = self.client.post('/applyjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'You have already applied for this job'})

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        payload = {'job_id':2}
        response = self.client.post('/applyjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'You have successfully applied for this job'})

        
    def test_applied_job(self):
        create_admin(**JobTestCase.recruiter)

        create_admin(**JobTestCase.testrecruiter)

        create_user(**JobTestCase.seeker)

        create_user(**JobTestCase.testseeker)

        payload = {'email':'recruiter@xyz.com','password':'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title':'Web developer','description':'We are looking for talented web developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','openings':1,'application_deadline':'2020-12-09'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = (response.content.decode('utf-8'))
        self.assertJSONEqual(response_content, {'message':'job details have been posted successfully'})

        payload = {'email':'testrecruiter@xyz.com','password':'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']
        
        payload = {'job_title':'Python developer','description':'We are looking for talented python developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','openings':2,'application_deadline':'2020-12-09'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'job details have been posted successfully'})

        # recruiter try to access applied jobs
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/appliedjobs/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'You need seeker privileges to perform this action'})

        payload = {'email':'seeker@abc.com','password':'Test@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        payload = {'job_id':1}
        response = self.client.post('/applyjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'You have successfully applied for this job'})

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        payload = {'job_id':2}
        response = self.client.post('/applyjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'You have successfully applied for this job'})

        # applied jobs
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/appliedjobs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content,[{'job_id':1, 'job_title':'Web developer','company':'ABC Tech Solutions',
                                                'applicant_id':3,'applicant_name':'seeker','applicant_email':'seeker@abc.com'},
                                                {'job_id':2, 'job_title':'Python developer','company':'ABC Tech Solutions',
                                                'applicant_id':3,'applicant_name':'seeker','applicant_email':'seeker@abc.com'}])


    def test_job_status_without_recruiter_access(self):
        create_admin(**JobTestCase.recruiter)

        create_admin(**JobTestCase.testrecruiter)

        create_user(**JobTestCase.seeker)

        create_user(**JobTestCase.testseeker)

        payload = {'email':'recruiter@xyz.com','password':'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title':'Web developer','description':'We are looking for talented web developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','openings':1,'application_deadline':'2020-12-09'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = (response.content.decode('utf-8'))
        self.assertJSONEqual(response_content, {'message':'job details have been posted successfully'})

        payload = {'email':'testrecruiter@xyz.com','password':'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']
        
        payload = {'job_title':'Python developer','description':'We are looking for talented python developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','openings':2,'application_deadline':'2020-12-09'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'job details have been posted successfully'})

        payload = {'email':'testseeker@abc.com','password':'Test@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/jobstatus/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'You need recruiter privileges to perform this action'})


    def test_job_status(self):
        create_admin(**JobTestCase.recruiter)

        create_admin(**JobTestCase.testrecruiter)

        create_user(**JobTestCase.seeker)

        create_user(**JobTestCase.testseeker)

        payload = {'email':'recruiter@xyz.com','password':'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title':'Web developer','description':'We are looking for talented web developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','openings':1,'application_deadline':'2020-12-09'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = (response.content.decode('utf-8'))
        self.assertJSONEqual(response_content, {'message':'job details have been posted successfully'})

        payload = {'email':'testrecruiter@xyz.com','password':'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']
        
        payload = {'job_title':'Python developer','description':'We are looking for talented python developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','openings':2,'application_deadline':'2020-12-09'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'job details have been posted successfully'})

        payload = {'email':'seeker@abc.com','password':'Test@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        payload = {'job_id':2}
        response = self.client.post('/applyjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'You have successfully applied for this job'})

        payload = {'email':'testseeker@abc.com','password':'Test@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        payload = {'job_id':2}
        response = self.client.post('/applyjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'You have successfully applied for this job'})

        payload = {'email':'testrecruiter@xyz.com','password':'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/myposts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content,[{'id':2,'job_title':'Python developer','company':'ABC Tech Solutions','description':'We are looking for talented python developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','about_company':'ABC Tech Solutions was established in 1996 to provides technology and consulting services',
                   'website':'http://www.abctech.com/','no_of_applicants':2,'openings':2,'application_deadline':'2020-12-09'}])

        # try to access other recruiters job status
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/jobstatus/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'You do not have permission to perform this action'})

        # job status
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/jobstatus/2/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, [{'job_id':2, 'job_title':'Python developer','company':'ABC Tech Solutions',
                                                'applicant_id':3,'applicant_name':'seeker','applicant_email':'seeker@abc.com'},
                                                {'job_id':2, 'job_title':'Python developer','company':'ABC Tech Solutions',
                                                'applicant_id':4,'applicant_name':'testseeker','applicant_email':'testseeker@abc.com'}])
        

    def test_view_profile_without_recruiter_access(self):
        create_user(**JobTestCase.testseeker)

        payload = {'email':'testseeker@abc.com','password':'Test@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/viewprofile/3/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'You need recruiter privileges to perform this action'})


    def test_view_profile(self):
        create_admin(**JobTestCase.recruiter)

        create_admin(**JobTestCase.testrecruiter)

        create_user(**JobTestCase.seeker)

        create_user(**JobTestCase.testseeker)


        payload = {'email':'testrecruiter@xyz.com','password':'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        # view profile
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/viewprofile/4/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'name':'testseeker','email':'testseeker@abc.com','date_of_birth':'1987-09-08','gender':'Male','mobile_number':8222222222,
                   'address':'Buldhana,Maharashtra','course':'BE','specialization':'Mechanical Engineer',
                   'course_type':'Full-time','college':'P R Pote','percentage':'97.00','year_of_passing':2020,'skills':'Python,Django,HTML,CSS',
                   'summary':'To achieve the objectives of the company with honesty and fairness','experience_level':'Fresher','designation':'System Engineer',
                   'responsibility':'As per requirement','company':'TCS','location':'Pune','worked_from':'2020-09-07','to':'2023-10-01'})
        
    
    def test_update_and_delete_job_without_recruiter_access(self):
        create_admin(**JobTestCase.recruiter)

        create_admin(**JobTestCase.testrecruiter)

        create_user(**JobTestCase.seeker)

        create_user(**JobTestCase.testseeker)

        payload = {'email':'recruiter@xyz.com','password':'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title':'Web developer','description':'We are looking for talented web developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','openings':1,'application_deadline':'2020-12-09'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = (response.content.decode('utf-8'))
        self.assertJSONEqual(response_content, {'message':'job details have been posted successfully'})

        payload = {'email':'testrecruiter@xyz.com','password':'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']
        
        payload = {'job_title':'Python developer','description':'We are looking for talented python developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','openings':2,'application_deadline':'2020-12-09'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'job details have been posted successfully'})

        payload = {'email':'testseeker@abc.com','password':'Test@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        payload = {'openings':1}
        response = self.client.patch('/updatejob/2/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'You need recruiter privileges to perform this action'})

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.delete('/updatejob/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_content = (response.content.decode('utf-8'))
        self.assertJSONEqual(response_content, {'message':'You need recruiter privileges to perform this action'})

    
    def test_update_and_delete_job(self):
        create_admin(**JobTestCase.recruiter)

        create_admin(**JobTestCase.testrecruiter)

        create_user(**JobTestCase.seeker)

        create_user(**JobTestCase.testseeker)

        payload = {'email':'recruiter@xyz.com','password':'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title':'Web developer','description':'We are looking for talented web developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','openings':1,'application_deadline':'2020-12-09'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = (response.content.decode('utf-8'))
        self.assertJSONEqual(response_content, {'message':'job details have been posted successfully'})

        payload = {'email':'testrecruiter@xyz.com','password':'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']
        
        payload = {'job_title':'Python developer','description':'We are looking for talented python developer capable of developing highily demanding applicants.'
                   'skills: Python,Django,REST APIs','experience':'0-1 years','work_location':'Pune','employment_type':'Full time',
                   'qualification':'B.E/B.Tech','openings':2,'application_deadline':'2020-12-09'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'job details have been posted successfully'})

        payload = {'openings':1}
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.patch('/updatejob/1/',data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'detail':'Authentication credentials were not provided.'})

        self.client.credentials(HTTP_AUTHORIZATION='Token iutgi')
        response = self.client.patch('/updatejob/1/',data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'detail':'Invalid token.'})


        payload = {'openings':1}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.patch('/updatejob/5/',data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'detail':'Not found.'})

        # try to update other recruiter job details
        payload = {'openings':1}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.patch('/updatejob/1/',data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'You do not have permission to perform this action'})

        #update
        payload = {'openings':1}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.patch('/updatejob/2/',data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'job details have been updated successfully'})

        
        # try to delete other recruiter job details
        payload = {'openings':1}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.delete('/updatejob/1/',data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message':'You do not have permission to perform this action'})

        #delete
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.delete('/updatejob/2/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
