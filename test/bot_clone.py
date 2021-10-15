import json
from pathlib import Path
import sys

from breaker_discord.client_breaker_audio_tts import ClientBreakerAudioTts
from breaker_discord.bot_clone import BotClone

from breaker_core.datasource.jsonqueue import Jsonqueue
from breaker_core.datasource.bytearraysource_generator import BytearraysourceGenerator

with open('config_aws.cfg', 'r') as file:
    dict_config = json.load(file)

jsonqueue_request = Jsonqueue.from_dict(dict_config['queue_request'])
bytearraysource_generator_voice = BytearraysourceGenerator.from_dict(dict_config['bsg_voice'])
bytearraysource_generator_output = BytearraysourceGenerator.from_dict(dict_config['bsg_output'])

client_tts = ClientBreakerAudioTts(jsonqueue_request)

bot = BotClone(
    dict_config['token'], 
    dict_config['path_file_ffmpef'],
    client_tts,
    bytearraysource_generator_voice,
    bytearraysource_generator_output)
bot.run()

