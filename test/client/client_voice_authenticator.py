from pathlib import Path
import random
import os
import json
import sys
import asyncio

from breaker_discord.client.client_voice_authenticator import ClientVoiceAuthenticator

from breaker_core.datasource.jsonqueue import Jsonqueue
from breaker_core.datasource.bytessource import Bytessource

path_file_config_breaker = os.environ['PATH_FILE_CONFIG_BREAKER_DEV']
with open(path_file_config_breaker, 'r') as file:
    dict_config = json.load(file)

jsonqueue_request = Jsonqueue.from_dict(dict_config['queue_request_voice_authenticator'])
bytessource_response = Bytessource.from_dict(dict_config['bytessource_response_voice_authenticator'])


bytessource_sound = Bytessource.from_dict(dict_config['bytessource_voice_sound'])
bytessource_encoding = Bytessource.from_dict(dict_config['bytessource_voice_encoding'])

client = ClientVoiceAuthenticator(jsonqueue_request, bytessource_response)
response = client.encode(
    bytessource_sound.join(['367', '367-130732-0000.flac']), 
    bytessource_encoding.join(['367', '367-130732-0000.flac']),
    force_reprocess=True)
print(response)

response = client.authenticate(
    bytessource_sound.join(['367', '367-130732-0000.flac']),
    bytessource_encoding.join(['1688']),
    force_reprocess=True)
print(response)
