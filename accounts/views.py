from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import *
from django.core.mail import send_mail
from django.contrib.auth import update_session_auth_hash
# from .signals import account_created
from .renderers import UserRenderer
from rest_framework.views import APIView

# Create your views here.
@api_view(["POST"])
def register_user(request):
    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            firstname = request.data.get("first_name")
            lastname = request.data.get("last_name")
            to = [request.data.get("email")]
            subject = "Account Registration Email"
            if request.data.get("roles") == "D":
                message = f"Hello Dr {firstname} {lastname} thanks for registering at HEALTH APP."
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=None,
                    recipient_list=to,
                    fail_silently=False,
                )
            else:
                message = f"Hello {firstname} {lastname} thanks for registering at HEALTH APP."
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=None,
                    recipient_list=to,
                    fail_silently=False,
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def user_login(request):
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")

        user = None
        if "@" in username:
            try:
                user = CustomUser.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)

        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == "POST":
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response(
                {"message": "Successfully logged out."}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# User Profile View Class 
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request , format=None):
        user = request.user 
        serializer = UserProfileSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post (self,request,format=None):
        serializer = UserChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid():
            return Response({"msg":"password changed successfully"} ,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        


        

# User Reset Password Classes 
# 1 ---> User Reset Password Request View 
class ResetPasswordRequestView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"msg":"Reset Password's Link Sent, Please Check Your Email BOX."},status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# 2 ---> User Reset Password View 
class ResetPasswordView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request ,uid, token, format=None):
        serializer = ResetPasswordSerializer(data=request.data, context={"uid":uid,"token":token})
        if serializer.is_valid():
            return Response({"msg":"password reset successfully"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

