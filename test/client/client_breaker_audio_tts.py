from pathlib import Path
import random
import json
import sys
import asyncio

from breaker_discord.client_breaker_audio_tts import ClientBreakerAudioTts

from breaker_core.datasource.jsonqueue import Jsonqueue
from breaker_core.datasource.bytessource_generator import BytessourceGenerator

with open('config_aws.cfg', 'r') as file:
    dict_config = json.load(file)

jsonqueue_request = Jsonqueue.from_dict(dict_config['queue_request'])
bytessource_generator_voice = BytessourceGenerator.from_dict(dict_config['bsg_voice'])
bytessource_generator_output = BytessourceGenerator.from_dict(dict_config['bsg_output'])

client = ClientBreakerAudioTts(jsonqueue_request)

list_list_key = bytessource_generator_voice.list_for_prefix(['voice'])
if len(list_list_key) == 0:
    raise Exception()

bytessource_voice = bytessource_generator_voice.generate(list_list_key[0])
bytessource_output = bytessource_generator_output.generate(['1634232048.wav'])

client.synthesize('eng', bytessource_voice, 'jaap is a super great programmer', bytessource_output)

print(bytessource_output.exists())