from django.db import models


class Yeelight(models.Model):
    id = models.IntegerField(primary_key=True)
    ip = models.GenericIPAddressField()
    name = models.CharField(max_length=32, null=True, blank=True)
    online = models.BooleanField(default=True)
