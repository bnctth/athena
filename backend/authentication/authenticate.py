import uuid
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.conf import settings
import jwt

from .models import AccessToken


class TokenBackend(BaseBackend):
    def authenticate(self, request, token=None):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(pk=payload["userID"])
            if user.is_active and AccessToken.objects.filter(aID=uuid.UUID(payload['jti'])).exists():
                return user
        except Exception as e:
            print(e)
            pass
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
