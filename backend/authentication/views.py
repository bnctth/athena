import datetime
import uuid

import jwt
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import authenticate

from authentication.decorator import login_required
from authentication.models import AccessToken, RefreshToken

ATEXP = getattr(settings, 'AUTH_ACCESS_TOKEN_EXPIRE_IN', 3600)
RTEXP = getattr(settings, 'AUTH_REFRESH_TOKEN_EXPIRE_IN', 60)


class Login(View):
    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            aID = uuid.uuid4()
            rID = uuid.uuid4()
            atPayload = {
                "exp": timezone.now() + datetime.timedelta(seconds=ATEXP),
                "userID": user.id,
                "jti": str(aID)
            }
            at = jwt.encode(atPayload, settings.SECRET_KEY, algorithm='HS256').decode()
            rtPayload = {
                'exp': timezone.now() + datetime.timedelta(days=RTEXP),
                'jti': str(rID),
            }
            rt = jwt.encode(rtPayload, settings.SECRET_KEY, algorithm='HS256').decode()
            atm = AccessToken.objects.create(user=user, aID=aID)
            rtm = RefreshToken.objects.create(aID=atm, rID=rID,
                                              expireAt=timezone.now() + datetime.timedelta(days=RTEXP),
                                              deviceName='Unknown')
            return JsonResponse({'access_token': at, 'expires_in': ATEXP, 'refresh_token': rt})
        return JsonResponse({'error': 'Invalid credentials'}, status=401)


class LoginRequiredTest(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return HttpResponse()
