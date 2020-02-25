import logging
import uuid
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import jwt

from .models import AccessToken

logger = logging.getLogger(__name__)


class TokenBackend(BaseBackend):
    def authenticate(self, request, token=None):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(pk=payload["userID"])
            if user.is_active and AccessToken.objects.filter(user=user, aID=uuid.UUID(payload['jti'])).exists():
                request.user = user
                request.token = token
                request.tokenPayload = payload
                return user
        except jwt.ExpiredSignature:
            logger.warning(f'Expired access token provided from {request.META["REMOTE_ADDR"]}')
        except (jwt.InvalidAlgorithmError, jwt.InvalidSignatureError, jwt.DecodeError,):
            logger.error(f'Invalid access token provided from {request.META["REMOTE_ADDR"]}')
        except ObjectDoesNotExist:
            logger.warning(f'Token for non-existent user provided from {request.META["REMOTE_ADDR"]}')
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
