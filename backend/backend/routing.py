from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from yeelight_smartlamp.consumer import YeelightConsumer

application = URLRouter([
    # USE WS/
    path('ws/yeelight', YeelightConsumer)
    # USE WS/
])
