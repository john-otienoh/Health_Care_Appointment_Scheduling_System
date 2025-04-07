from django.urls import path
from .views import *

urlpatterns = [
    path("register/", register_user, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path('profile/', UserProfileView.as_view() ,name="profile"),
    path('change_password/',UserChangePasswordView.as_view(),name="change_password"),
    path('reset-password/' , ResetPasswordRequestView.as_view(),name="reset-password"),
    path('reset-password/<uid>/<token>/', ResetPasswordView.as_view(),name='reset-password-done'),
]
