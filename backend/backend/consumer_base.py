import json
import logging
from json import JSONDecodeError

from asgiref.sync import async_to_sync
from django.contrib.auth import authenticate

logger = logging.getLogger(__name__)


def authenticatedWS(self, text_data, processor):
    try:
        decoded = json.loads(text_data)
        if self.user.is_authenticated:
            processor(self, decoded)
        elif decoded['type'] == 'authenticate':
            user = authenticate(token=decoded['access_token'])
            if user:
                async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
                self.user = user
                self.send(json.dumps({'type': 'authenticate', 'status': 'logged in'}))
                return
            else:
                self.send(json.dumps({'type': 'error', 'error': 'wrong credential'}))
        else:
            self.send(json.dumps({'type': 'error', 'error': 'not authenticated'}))
    except JSONDecodeError:
        logger.exception('could not decode the text')
        self.send(json.dumps({'type': 'error', 'error': 'wrong format'}))
    except KeyError:
        logger.exception('could not get the needed key')
        self.send(json.dumps({'type': 'error', 'error': 'wrong format'}))
