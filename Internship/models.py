from django.db import models

# Create your models here.

class Internship(models.Model):
    company_name = models.CharField(max_length=300)
    address = models.CharField(max_length=500)
    email = models.EmailField()
    contact_number = models.IntegerField()
    website = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name
