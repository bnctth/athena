import json
import logging
from json import JSONDecodeError

from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser

from backend.consumer_base import receive

logger = logging.getLogger(__name__)


class YeelightConsumer(WebsocketConsumer):
    def connect(self):
        self.user = AnonymousUser()
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        def processor(s, decoded):
            s.send(decoded['type'])

        receive(self, text_data, processor)
