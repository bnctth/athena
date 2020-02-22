from django.contrib import admin

# Register your models here.
from authentication.models import AccessToken, RefreshToken

admin.site.register(AccessToken)
admin.site.register(RefreshToken)
