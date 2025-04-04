from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import Signal

# account_created = Signal(providing_args=["user", "request"])

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    """
    Send password reset email with token link.
    
    Args:
        sender: View class that sent the signal
        instance: View instance that sent the signal
        reset_password_token: Token Model object
        **kwargs: Additional arguments
    """
    context = {
        "user": reset_password_token.user,
        "reset_password_url": build_reset_url(instance, reset_password_token.key),
        "site_name": getattr(settings, "SITE_NAME", "Our Site"),
        "support_email": getattr(settings, "SUPPORT_EMAIL", "support@example.com"),
    }
    email_messages = render_email_templates(context)
    send_reset_email(reset_password_token.user.email, email_messages, context["site_name"])
 
def build_reset_url(instance, token):
    """Construct the password reset URL."""
    relative_url = reverse("password_reset:reset-password-confirm")
    return f"{instance.request.build_absolute_uri(relative_url)}?token={token}"

def render_email_templates(context):
    """Render both HTML and plaintext email templates."""
    return {
        "html": render_to_string("accounts/emails/password_reset.html", context),
        "text": render_to_string("accounts/emails/password_reset.txt", context),
    }

def send_reset_email(recipient, email_messages, site_name):
    """Send the password reset email."""
    msg = EmailMultiAlternatives(
        subject=f"Password Reset for {site_name}",
        body=email_messages["text"],
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@example.com"),
        to=[recipient],
    )
    msg.attach_alternative(email_messages["html"], "text/html")
    msg.send()
