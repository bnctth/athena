from base64 import b64encode

from django.db import models


# Create your models here.
class Yeelight(models.Model):
    id = models.IntegerField(primary_key=True)
    ip = models.GenericIPAddressField()
    name = models.CharField(max_length=32, null=True, blank=True)
