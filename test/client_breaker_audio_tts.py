from pathlib import Path
import random
import json
import sys
import asyncio

from breaker_discord.client_breaker_audio_tts import ClientBreakerAudioTts

from breaker_core.datasource.jsonqueue import Jsonqueue
from breaker_core.datasource.bytearraysource_generator import BytearraysourceGenerator

with open('config_aws.cfg', 'r') as file:
    dict_config = json.load(file)

jsonqueue_request = Jsonqueue.from_dict(dict_config['queue_request'])
bytearraysource_generator_voice = BytearraysourceGenerator.from_dict(dict_config['bsg_voice'])
bytearraysource_generator_output = BytearraysourceGenerator.from_dict(dict_config['bsg_output'])

client = ClientBreakerAudioTts(jsonqueue_request)

list_list_key = bytearraysource_generator_voice.list_for_prefix(['voice'])
if len(list_list_key) == 0:
    raise Exception()

bytearraysource_voice = bytearraysource_generator_voice.generate(list_list_key[0])
bytearraysource_output = bytearraysource_generator_output.generate(['1634232048.wav'])

client.synthesize('eng', bytearraysource_voice, 'jaap is a super great programmer', bytearraysource_output)

print(bytearraysource_output.exists())