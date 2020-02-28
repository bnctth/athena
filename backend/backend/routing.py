from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

from yeelight_smartlamp.consumer import YeelightConsumer

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        url('yeelight', YeelightConsumer)
    ])
})
