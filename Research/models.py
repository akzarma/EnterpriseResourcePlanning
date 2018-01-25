import datetime

from django.db import models
from django.utils import timezone

from Registration.models import Faculty


def faculty_directory_path(instance, filename):
    return 'Media/Faculty/{0}/Research/{1}'.format(instance.faculty.faculty_code, filename)


class Paper(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True, blank=True)
    year = models.PositiveIntegerField(default=timezone.now().year)
    date = models.DateField(default=timezone.now)
    type = models.CharField(max_length=10)  # Paid/Unpaid
    title = models.CharField(max_length=200)
    medium = models.CharField(max_length=50)  # Journal/Conference
    conference_attended = models.BooleanField(default=False)  # Has attended the conference
    level = models.CharField(max_length=50)  # National/International
    medium_name = models.CharField(max_length=200)  # Journal/Conference Name
    distribution = models.CharField(max_length=50)  # Online/Print
    peer_reviewed = models.BooleanField()  # Yes/No
    isbn = models.CharField(max_length=25)
    impact_factor = models.FloatField()
    volume = models.CharField(max_length=20)
    domain = models.CharField(max_length=100)
    paper_with = models.CharField(max_length=20)  # BE Student/ ME Student/ PhD Student/ Self
    first_author = models.BooleanField()
    funds_from_college = models.PositiveIntegerField()
    other_info = models.CharField(max_length=200)
    files = models.FileField(upload_to=faculty_directory_path, null=True, blank=True)
