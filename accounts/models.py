from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

ROLES = [("D", "Doctor"), ("P", "Patient")]


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    roles = models.CharField(choices=ROLES, max_length=2, default=ROLES[0][0])

    def __str__(self):
        return self.username
