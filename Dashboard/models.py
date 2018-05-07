from django.db import models

# Create your models here.
from UserModel.models import User


class SpecificNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    notification = models.CharField(max_length=5000)
    heading = models.CharField(max_length=100)
    action = models.CharField(max_length=500,default='')
    type = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=1)
    has_read = models.BooleanField(default=False)

    def __str__(self):
        return self.heading + self.user.faculty.initials

