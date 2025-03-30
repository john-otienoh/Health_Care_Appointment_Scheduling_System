from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.
ROLES = [("D", "Doctor"), ("P", "Patient")]


class User(AbstractUser):
    roles = models.CharField(choices=ROLES, max_length=2)

    def doctor(self):
        return True if self.roles == "D" else False

    def patient(self):
        return True if self.roles == "P" else False

    class Meta:
        ordering = ("id",)
