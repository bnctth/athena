import logging

from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import AnonymousUser

from backend.consumer_base import authenticatedWS

logger = logging.getLogger(__name__)


class YeelightConsumer(WebsocketConsumer):
    def connect(self):
        self.user = AnonymousUser()
        self.accept()
        self.group_name = 'yeelight'

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        def processor(s, decoded):
            s.send(decoded['type'])

        authenticatedWS(self, text_data, processor)
