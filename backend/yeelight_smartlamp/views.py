from base64 import b64decode

import yeelight
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator

from authentication.decorator import login_required
from yeelight_smartlamp.lamp_manager import Lamp, addLamp
from yeelight_smartlamp.models import Yeelight
from django.views import View


def b64NameToPlain(name):
    return b64decode(name).encode('utf-8') if name else 'Unset'


class Search(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        bulbs = yeelight.discover_bulbs()
        resp = []
        for b in bulbs:
            if not Yeelight.objects.filter(id=int(b['capabilities']['id'], 16)).exists():
                name = b64NameToPlain(b['capabilities']['name'])
                resp.append({
                    'name': name,
                    'id': int(b['capabilities']['id'], 16),
                    'model': b['capabilities']['model']
                })
        return JsonResponse(resp, safe=False)


class AddLamp(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        id = int(request.POST.get('id'))
        if Yeelight.objects.filter(id=id).exists(): return HttpResponse()
        bulbs = yeelight.discover_bulbs()
        for b in bulbs:
            if int(b['capabilities']['id'], 16) == id:
                lamp = Yeelight.objects.create(id=int(b['capabilities']['id'], 16), ip=b['ip'], online=True,
                                               name=b64NameToPlain(b['capabilities']['name']))
                lamp.save()
                addLamp(Lamp(lamp))
                return HttpResponse()
        return HttpResponse(400)
