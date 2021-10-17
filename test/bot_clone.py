import json
from pathlib import Path
import sys

from breaker_core.datasource.jsonqueue import Jsonqueue
from breaker_core.datasource.bytearraysource import Bytearraysource


from breaker_discord.client_breaker_audio_tts import ClientBreakerAudioTts
from breaker_discord.command.command_play import CommandPlay
from breaker_discord.command.command_play import CommandPlaylist
from breaker_discord.command.command_play import CommandPlayalias
from breaker_discord.bot_clone import BotClone
 
with open('config.cfg', 'r') as file:
    dict_config = json.load(file)

token = dict_config['token']
path_file_ffmpef = Path(dict_config['path_file_ffmpef'])
jsonqueue_request = Jsonqueue.from_dict(dict_config['queue_request'])
bytearraysource_voice = Bytearraysource.from_dict(dict_config['bytearraysource_voice'])
bytearraysource_sound = Bytearraysource.from_dict(dict_config['bytearraysource_sound'])
bytearraysource_output_tts = Bytearraysource.from_dict(dict_config['bytearraysource_output_tts'])

client_tts = ClientBreakerAudioTts(jsonqueue_request)

bot = BotClone(
    token, 
    path_file_ffmpef,
    client_tts,
    bytearraysource_voice,
    bytearraysource_output_tts)
bot.run()

