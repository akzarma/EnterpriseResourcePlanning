from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from General.models import Division, Batch
from Registration.models import Branch


class SpecificNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    notification = models.CharField(max_length=5000)
    heading = models.CharField(max_length=100)
    action = models.CharField(max_length=500,default='')
    type = models.CharField(max_length=200, null=True)
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=1)
    has_read = models.BooleanField(default=False)

    def __str__(self):
        str = self.heading
        if self.user.faculty:
            str += self.user.faculty.initials
        else:
            str += self.user.student.gr_number
        return str


class GeneralStudentNotification(models.Model):
    datetime = models.DateTimeField()
    notification = models.CharField(max_length=5000)
    heading = models.CharField(max_length=100)
    action = models.CharField(max_length=500, default='')
    type = models.CharField(max_length=200, null=True)
    priority = models.IntegerField(default=1)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True)
    batch = models.ForeignKey(Batch, null=True,blank=True,on_delete=models.CASCADE)
    for_batch = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.action


class GeneralFacultyNotification(models.Model):
    datetime = models.DateTimeField()
    notification = models.CharField(max_length=5000)
    heading = models.CharField(max_length=100)
    action = models.CharField(max_length=500, default='')
    type = models.CharField(max_length=200, null=True)
    priority = models.IntegerField(default=1)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.action
