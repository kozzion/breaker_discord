import json
from pathlib import Path
import sys

from breaker_core.datasource.jsonqueue import Jsonqueue
from breaker_core.datasource.bytearraysource import Bytearraysource


from breaker_discord.client.client_breaker_audio_tts import ClientBreakerAudioTts

from breaker_discord.command.command_admin import CommandHelp
from breaker_discord.command.command_admin import CommandJoin
from breaker_discord.command.command_admin import CommandLeave

from breaker_discord.command.command_admin import CommandAliasme
from breaker_discord.command.command_admin import CommandAliaslist

from breaker_discord.command.command_play import CommandPlay
from breaker_discord.command.command_play import CommandPlaylist

from breaker_discord.command.command_post import CommandPost
from breaker_discord.command.command_post import CommandPostlist


from breaker_discord.command.command_ai import CommandTts
from breaker_discord.command.command_ai import CommandPlayme
from breaker_discord.command.command_ai import CommandPlayuser

# from breaker_discord.command.command_play import CommandPlayalias
from breaker_discord.bot_clone import BotClone

with open('config_dev.cfg', 'r') as file:
    dict_config = json.load(file)

token = dict_config['token']
path_file_ffmpef = Path(dict_config['path_file_ffmpef'])
jsonqueue_tts = Jsonqueue.from_dict(dict_config['queue_request_tts'])

bytearraysource_output_tts = Bytearraysource.from_dict(dict_config['bytearraysource_output_tts'])
bytearraysource_bot = Bytearraysource.from_dict(dict_config['bytearraysource_bot'])
bytearraysource_voice = bytearraysource_bot.join(['voice'])
bytearraysource_sound = bytearraysource_bot.join(['sound'])
bytearraysource_file = bytearraysource_bot.join(['file'])

client_tts = ClientBreakerAudioTts(jsonqueue_tts)

bot = BotClone(
    token, 
    path_file_ffmpef,
    bytearraysource_bot)

bot.add_command(CommandHelp())
bot.add_command(CommandJoin())
bot.add_command(CommandLeave())

bot.add_command(CommandAliasme())
bot.add_command(CommandAliaslist())

bot.add_command(CommandPlay(bytearraysource_sound))
bot.add_command(CommandPlaylist(bytearraysource_sound))

bot.add_command(CommandPost(bytearraysource_file))
bot.add_command(CommandPostlist(bytearraysource_file))

bot.add_command(CommandTts(client_tts, bytearraysource_voice, bytearraysource_output_tts))
bot.add_command(CommandPlayme(bytearraysource_voice))
bot.add_command(CommandPlayuser(bytearraysource_voice))



# bot.add_command(CommandPlayalias(bytearraysource_sound))
bot.run()

