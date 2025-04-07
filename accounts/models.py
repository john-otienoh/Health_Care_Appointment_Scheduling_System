from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.core.validators import RegexValidator

# Create your models here.

ROLES = [("D", "Doctor"), ("P", "Patient")]
GENDER = [("M", "Male"), ("F", "Female"), ("O", "Other")]
BLOOD_GROUPS = [
    ("O-", "O-"),
    ("O+", "O+"),
    ("A-", "A-"),
    ("A+", "A+"),
    ("B-", "B-"),
    ("B+", "B+"),
    ("AB-", "AB-"),
    ("AB+", "AB+"),
]


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    roles = models.CharField(choices=ROLES, max_length=2, default=ROLES[0][0])

    def __str__(self):
        return self.username

def user_directory_path(instance, filename):
    return f"user_{instance.user.id}/{filename}"


class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=50)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    gender = models.CharField(choices=GENDER, max_length=1)
    age = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=50, blank=True)
    blood_group = models.CharField(choices=BLOOD_GROUPS, max_length=3, blank=True)
    med_reps = models.FileField(upload_to="profile/med_reps", blank=True)
    specialization = models.CharField(max_length=100)
    registration_number = models.IntegerField()
    years_of_experience = models.IntegerField()
    next_of_kin = models.CharField(max_length=50)
    insurance_number = models.IntegerField()
    certifications = models.FileField(upload_to=user_directory_path)
    avatar = models.ImageField(default="default.jpg", upload_to="profile_images")
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
