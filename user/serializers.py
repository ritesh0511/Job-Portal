from django.contrib.auth import get_user_model,authenticate
#from django.utils.translation import ugettext_lazy
from rest_framework import serializers

from user.models import UserDetails


class RecruiterSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserDetails
        fields = ['name','designation','company','email','date_of_birth','gender','mobile_number','about_company','website','password']
        extra_kwargs = {'password':{'write_only':True}}


class UserSerializer(serializers.ModelSerializer): 

    class Meta:
        model = UserDetails
        exclude = ['id','is_active','is_staff','about_company','website','groups','user_permissions','last_login','is_superuser']
        extra_kwargs = {'password':{'write_only':True}}


class AuthTokenSerializer(serializers.Serializer):

    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, request):
        email = request.get('email')
        try:
            user = get_user_model().objects.get(email=email)
            if user.check_password(request.get('password')):
                request['user'] = user
                return request
        except get_user_model().DoesNotExist:
            msg = {'non_field_errors':'Unable to authentiacate with provided credentials'}
            raise serializers.ValidationError(msg, code='authorization')
            
        else:
            msg = {'non_field_errors':'Unable to authenticate with provided credentials'}
            raise serializers.ValidationError(msg, code='authorization')
