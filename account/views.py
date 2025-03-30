from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.views import View
from .forms import *
from .models import User

# Create your views here.


def home(request):
    return render(request, "account/home.html")


def about(request):
    return render(request, "account/about.html")


def contact(request):
    return render(request, "account/contact.html")


class RegisterView(View):
    form_class = RegisterForm
    initial = {"key": "value"}
    template_name = "registration/signup.html"

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to="/")

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()

            firstname = form.cleaned_data.get("first_name")
            lastname = form.cleaned_data.get("last_name")
            username = form.cleaned_data.get("username")
            to = [form.cleaned_data.get("email")]
            subject = "Account Registration Email"

            if form.cleaned_data.get("roles") == "D":
                message = f"""
                    Hello Dr {firstname} {lastname}.
                    Thank you for registering at Health  App
                    We care for your Cure.
                """
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=None,
                    recipient_list=to,
                    fail_silently=False,
                )
            else:
                message = f"""
                    Hello {firstname} {lastname}.
                    Thank you for registering at Health  App.
                    We care for your Cure.
                """
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=None,
                    recipient_list=to,
                    fail_silently=False,
                )
            messages.succcess(request, f"Account created for {username}")
            return redirect(to="account:login")
        return render(request, self.template_name, {"form": form})


class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)
