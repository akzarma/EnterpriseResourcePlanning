from django.db import models

# Create your models here.
from Registration.models import Branch


class Internship(models.Model):
    company_name = models.CharField(max_length=300)
    address = models.CharField(max_length=500)
    email = models.EmailField()
    contact_number = models.IntegerField()
    website = models.CharField(max_length=50)
    branch = models.ForeignKey(Branch, blank=True,on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.company_name
