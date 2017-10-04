from datetime import datetime

from django.db import models

# Create your models here.
from Registration.models import Faculty


def faculty_papers_path(instance, filename):
    return 'Media/Faculty/{0}/{1}'.format(instance.faculty.user.first_name, filename)


class Paper(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, blank=True)
    publication_year = models.PositiveIntegerField(default=datetime.now().year)
    publication_date = models.DateField(default=datetime.now)
    type = models.CharField(max_length=10)
    title = models.CharField(max_length=150)
    conference_name = models.CharField(max_length=150)
    conference_type = models.CharField(max_length=20)
    peer_reviewed = models.CharField(max_length=10)
    publication_medium = models.CharField(max_length=10)
    isbn = models.PositiveIntegerField()
    domain = models.CharField(max_length=100)
    funds_received_from_college = models.PositiveIntegerField()
    other_info = models.TextField()
    files = models.FileField(upload_to=faculty_papers_path, null=True, blank=True)
