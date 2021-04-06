from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User, auth
# Create your models here.

class User(AbstractUser):
    manager = models.CharField(max_length=100, null=True)
    designation = models.CharField(max_length=100, null=True)
    date_of_birth = models.DateField(null=True)
    profile_image = models.ImageField(default="profileDefault.jpg", null=True)

    @property
    def ImageURL(self):
        try:
            url = self.profile_image.url
        except ValueError:
            url = ''
        return url
