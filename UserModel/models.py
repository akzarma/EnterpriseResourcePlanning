from django.contrib.auth.models import AbstractUser, UserManager, User
from django.db import models


# Create your models here.


class RoleMaster(models.Model):
    role = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True,blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.role

class RoleManager(models.Model):
    user_obj = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    role = models.ForeignKey(RoleMaster, on_delete=models.CASCADE)

    def __str__(self):
        return self.role.role