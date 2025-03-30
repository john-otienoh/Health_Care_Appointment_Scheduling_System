from django.contrib.auth import views as auth_views
from django.urls import path
from .views import *

app_name = "account"

urlpatterns = [
    path("home/", home, name="home"),
    path("about/", about, name="about"),
    path("contact/", contact, name="contact"),
    path("register/", RegisterView.as_view(), name="registration"),
    path(
        "login/",
        CustomLoginView.as_view(
            redirect_authenticated_user=True,
            template_name="users/login.html",
            authentication_form=LoginForm,
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="registration/logout.html"),
        name="logout",
    ),
]
