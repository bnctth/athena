import datetime
import logging
import uuid

import jwt
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate

from authentication.decorator import login_required
from authentication.models import AccessToken, RefreshToken

ATEXP = getattr(settings, 'AUTH_ACCESS_TOKEN_EXPIRE_IN', 3600)
RTEXP = getattr(settings, 'AUTH_REFRESH_TOKEN_EXPIRE_IN', 60)

logger = logging.getLogger(__name__)


class Login(View):
    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            logger.info(f'{user} logged in from {request.META["REMOTE_ADDR"]}')
            at, rt, aID, rID = createTokens(user)
            atm = AccessToken.objects.create(user=user, aID=aID)
            RefreshToken.objects.create(aID=atm, rID=rID,
                                        expireAt=timezone.now() + datetime.timedelta(days=RTEXP),
                                        deviceName='Unknown')
            return JsonResponse({'access_token': at, 'expires_in': ATEXP, 'refresh_token': rt})
        logger.warning(
            f'Failed login attempt from {request.META["REMOTE_ADDR"]}, the provided username was: {username}')
        return JsonResponse({'error': 'Invalid credentials'}, status=401)


# generates an access and a refresh token
def createTokens(user):
    aID = uuid.uuid4()
    rID = uuid.uuid4()
    atPayload = {
        "exp": timezone.now() + datetime.timedelta(seconds=ATEXP),
        "userID": user.id,
        "jti": str(aID),
        "type": "access_token",
    }
    at = jwt.encode(atPayload, settings.SECRET_KEY, algorithm='HS256').decode()
    rtPayload = {
        'exp': timezone.now() + datetime.timedelta(days=RTEXP),
        'jti': str(rID),
        'type': 'refresh_token',
    }
    rt = jwt.encode(rtPayload, settings.SECRET_KEY, algorithm='HS256').decode()
    return at, rt, aID, rID


# gives new at rt
class RenewToken(View):
    def post(self, request, *args, **kwargs):
        rt = request.POST.get('refresh_token')
        try:
            payload = jwt.decode(rt, settings.SECRET_KEY, algorithms=['HS256'])
            rtm = RefreshToken.objects.get(rID=payload['jti'])
            user = rtm.aID.user
        except jwt.ExpiredSignature:
            logger.warning(f'Expired refresh token provided from {request.META["REMOTE_ADDR"]}')
            return JsonResponse({'error': 'Expired refresh token'}, status=401)
        except (jwt.DecodeError, jwt.InvalidSignatureError, jwt.InvalidAlgorithmError, ObjectDoesNotExist):
            logger.warning(f'Invalid refresh token provided from {request.META["REMOTE_ADDR"]}')
            return JsonResponse({'error': 'Invalid refresh token'}, status=401)
        at, rt, aID, rID = createTokens(user)
        rtm.rID = rID
        rtm.aID.aID = aID
        rtm.expireAt = timezone.now() + datetime.timedelta(days=RTEXP)
        rtm.save()
        rtm.aID.save()
        return JsonResponse({'access_token': at, 'expires_in': ATEXP, 'refresh_token': rt})


class Logout(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        atm = AccessToken.objects.get(aID=uuid.UUID(request.tokenPayload['jti']))
        logger.info(f'{request.user} logged out from {RefreshToken.objects.get(aID=atm).deviceName}')
        atm.delete()
        return HttpResponse()


# get id for log out device
class GetRTPKs(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        response = []
        for rtm in RefreshToken.objects.all():
            if rtm.aID.user == request.user:
                response.append({'pk': rtm.pk, 'device_name': rtm.deviceName})
        return JsonResponse(response, safe=False)


# log out a specific device
class LogoutByRTPK(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        try:
            rt = RefreshToken.objects.get(pk=pk)
        except ObjectDoesNotExist:
            logger.warning(f'from {request.META["REMOTE_ADDR"]} {request.user} tried to log out a device with bad id')
            return JsonResponse({'error': 'Invalid id'}, status=400)
        logger.info(f'{request.user} logged out their device: {rt.deviceName}')
        rt.aID.delete()
        return HttpResponse()


class LogoutEverywhereElse(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        AccessToken.objects.exclude(aID=uuid.UUID(request.tokenPayload['jti'])).delete()
        logger.info(f'{request.user} logged out from everywhere except {request.META["REMOTE_ADDR"]}')
        return HttpResponse()


class ChangePassword(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        oldPasswd = request.POST.get("old_password")
        newPasswd = request.POST.get("new_password")
        if request.user.check_password(oldPasswd):
            request.user.set_password(newPasswd)
            request.user.save()
            logger.info(f'{request.user} has changed their password from {request.META["REMOTE_ADDR"]}')
            return HttpResponse()
        return JsonResponse({'error': 'Incorrect password'}, status=401)


# just a simple test function
class LoginRequiredTest(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return HttpResponse()
