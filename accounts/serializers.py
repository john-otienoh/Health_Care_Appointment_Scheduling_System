from rest_framework import serializers
from xml.dom import ValidationErr
from .models import *
from django.utils.encoding import force_bytes , smart_str , DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode , urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util 
from django.utils.encoding import force_bytes , smart_str , DjangoUnicodeDecodeError

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type' : 'password'}, write_only=True)
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "username", "email", "password", "password2", "roles"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError('Your password and confirm password are not match')
        return attrs
    
    def create(self, validated_data):
        user = CustomUser(
            username=validated_data["username"],
            email=validated_data["email"],
            roles=validated_data["roles"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        # fields = ['name', 'phone_number', 'gender', 'age', 'address', 'blood_group', 'avatar']
        fields = '__all__'
        
class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 255,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length = 255,style={'input_type':'password'},write_only=True)
    class Meta:
        model = CustomUser
        fields = ['password','password2']
    
    # Check the Validation Between User's Password and Confirm Password  
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('Your Password and confirm Password Doesn\'t Match!')
        user.set_password(password)
        user.save()
        return attrs
    
class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = CustomUser
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print("user id encoded, and it's: ",uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('password reset token: ',token)
            link = "http://localhost:3000/Api/resetpassword/"+uid+'/'+token
            print('password reset link: ',link)  
            body = 'Hello Dear , Click on the following link to reset your password' + '\n' + link
            data = {
                'subject':'Django Reset Password',
                'body' : body,
                'to_email' : user.email
            }
            Util.email_sender(data)
            return attrs
        else:
            raise ValidationErr('User Doesn\'t exist! ')




 

# User Reset Password Serializer 
class ResetPasswordSerializer(serializers.Serializer): 
    password = serializers.CharField(max_length = 255,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length = 255,style={'input_type':'password'},write_only=True)
    class Meta:
        model = CustomUser
        fields = ['password','password2']
    
    # Check the Validation Between User's New Password and Confirm New Password  
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        uid = self.context.get('uid')
        token = self.context.get('token')

        if password != password2:
            raise serializers.ValidationError('Your Password and confirm Password Doesn\'t Match!')
        # decoding the uid and find the specific user
        id = smart_str(urlsafe_base64_decode(uid))
        user = CustomUser.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user,token):
            raise serializers.ValidationError('Token is Expired or Invalid')
        user.set_password(password)
        user.save()
        return attrs
    