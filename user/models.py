from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.core.validators import RegexValidator,EmailValidator


# create Token for every user automatically+

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)

# Create your models here.

class UserManager(BaseUserManager):
    # custom user model
    
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('users must have an email address')
        user = self.model(email = self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_admin(self,email,password=None,**extra_fields):
        return self.create_user(email,password,**extra_fields,is_staff= True)
    
class UserDetails(AbstractBaseUser,PermissionsMixin):

    id = models.AutoField(primary_key=True,)
    name = models.CharField(max_length=140,validators=[RegexValidator(regex='^([A-Za-z]+){4,}$', message='Enter a valid name')])
    email = models.CharField(max_length=140,validators=[EmailValidator(message='Enter a valid email')],unique=True)
    date_of_birth = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=140)
    mobile_number = models.IntegerField(validators=[RegexValidator(regex=r'^([789])?\d{10}$',message='Enter a valid mobile number')],unique=True)
    address = models.TextField(null=True,blank=True)
    password = models.CharField(max_length=140,validators=[RegexValidator(regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$&*?])[a-zA-Z\d!@#$&*?]{6,}',message='Enter a valid password')])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    course = models.CharField(max_length=140,null=True,blank=True)
    specialization = models.CharField(max_length=140,null=True,blank=True)
    course_type = models.CharField(max_length=140,null=True,blank=True)
    college = models.CharField(max_length=140,null=True,blank=True)
    percentage = models.DecimalField(null=True,blank=True,max_digits=4,decimal_places=2)
    year_of_passing = models.IntegerField(null=True,blank=True)
    skills = models.CharField(null=True,blank=True,max_length=140)
    summary = models.TextField(null=True,blank=True)
    experience_level = models.CharField(max_length=140,null=True,blank=True)
    designation = models.CharField(max_length=140,null=True,blank=True)
    responsibility = models.TextField(null=True,blank=True)
    company = models.CharField(max_length=140,null=True,blank=True)
    location = models.CharField(max_length=140,null=True,blank=True)
    worked_from = models.DateField(null=True,blank=True)
    to = models.DateField(null=True,blank=True)
    about_company = models.TextField(null=True,blank=True)
    website = models.URLField(null=True,blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email
