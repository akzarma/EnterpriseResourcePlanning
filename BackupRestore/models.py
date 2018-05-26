from django.db import models

# Create your models here.
from EnterpriseResourcePlanning.settings import PROJECT_ROOT


class Backup(models.Model):
    version = models.FloatField(unique=True)
    date = models.DateTimeField()
    is_latest = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    # location = models.FilePathField(path=PROJECT_ROOT + '/BackupRestore/db')

    def __str__(self):
        return str(self.version) + ' ' + str(self.date)
