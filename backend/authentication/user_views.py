import logging
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View

from authentication.decorator import login_required
from authentication.models import RefreshToken, AccessToken

logger = logging.getLogger(__name__)


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
        logger.warning(f'{request.user} tried to change their password unsuccessfully')
        return JsonResponse({'error': 'Incorrect password'}, status=401)
