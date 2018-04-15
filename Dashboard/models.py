from django.db import models

# Create your models here.
from UserModel.models import User


class SpecificNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.CharField(max_length=5000)
    type = models.CharField(max_length=100)
    action = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)
