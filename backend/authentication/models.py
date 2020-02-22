from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class AccessToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    aID = models.UUIDField()


class RefreshToken(models.Model):
    expireAt = models.DateTimeField()
    rID = models.UUIDField()
    aID = models.ForeignKey(AccessToken, on_delete=models.CASCADE)
    deviceName = models.CharField(max_length=100)
