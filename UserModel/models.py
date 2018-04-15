from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


# Create your models here.

class User(AbstractUser):
    role = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()


