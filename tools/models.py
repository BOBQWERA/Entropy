from django.db import models

from django.utils import timezone
from datetime import timedelta


class Tools(models.Model):
    name = models.CharField(max_length=10)
    url = models.CharField(max_length=10)


class Files(models.Model):
    name = models.CharField(max_length=20,null=True)
    password = models.CharField(max_length=20,null=True)
    file = models.FileField(upload_to='uploads/')

    class Meta:
        db_table = 'files_storage'
        ordering = ['-id']
    