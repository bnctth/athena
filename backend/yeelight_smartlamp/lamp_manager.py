from base64 import b64decode

import yeelight

from yeelight_smartlamp.models import Yeelight


class Lamp:
    def __init__(self, lamp):
        self.id = lamp.id
        self.bulb = yeelight.Bulb(lamp.ip)


def b64NameToPlain(name):
    return b64decode(name).encode('utf-8') if name else 'Unset'


def refresh():
    bulbs = yeelight.discover_bulbs()
    for b in bulbs:
        if Yeelight.objects.filter(id=int(b['capabilities']['id'], 16)).exists():
            lamp = Yeelight.objects.get(id=int(b['capabilities']['id'], 16))
            lamp.ip = b['ip']
            lamp.online = True
            lamp.name = b64NameToPlain(b['capabilities']['name'])
            lamp.save()


LAMPS = []


def addLamp(lamp):
    LAMPS.append({
        lamp.id: lamp
    })

