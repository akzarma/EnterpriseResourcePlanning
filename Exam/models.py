from django.db import models


# Create your models here.
from General.models import CollegeExtraDetail


class ExamMaster(models.Model):
    exam_name = models.CharField(max_length=300)
    # Below 2 fields would be filled ate the time of active/inactive
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)


class ExamDetail(models.Model):
    exam = models.ForeignKey(ExamMaster)
    year = models.ForeignKey(CollegeExtraDetail)
    schedule_start_date = models.DateField()
    schedule_end_date = models.DateField()
