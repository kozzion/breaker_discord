
import sys
import os
import json
from pathlib import Path

from breaker_core.datasource.jsonqueue import Jsonqueue
from breaker_core.datasource.bytessource import Bytessource


from breaker_discord.client.client_breaker_audio_tts import ClientBreakerAudioTts
from breaker_discord.client.client_voice_authenticator import ClientVoiceAuthenticator

from breaker_discord.agent.agent_logger import AgentLoggerEvent

from breaker_discord.command.command_admin import CommandHelp
from breaker_discord.command.command_admin import CommandJoin
from breaker_discord.command.command_admin import CommandLeave
from breaker_discord.command.command_admin import CommandAliasme
from breaker_discord.command.command_admin import CommandAliaslist

from breaker_discord.command.command_log import CommandLogplotevent

from breaker_discord.command.command_play import CommandPlay
from breaker_discord.command.command_play import CommandPlaylist

from breaker_discord.command.command_post import CommandPost
from breaker_discord.command.command_post import CommandPostlist


from breaker_discord.command.command_ai import CommandTts
from breaker_discord.command.command_ai import CommandRecordme
from breaker_discord.command.command_ai import CommandPlayme
from breaker_discord.command.command_ai import CommandPlayuser
from breaker_discord.command.command_ai import CommandVoiceauth

# from breaker_discord.command.command_play import CommandPlayalias
from breaker_discord.bot_clone import BotClone

path_file_config_breaker = os.environ['PATH_FILE_CONFIG_BREAKER_DEV']
with open(path_file_config_breaker, 'r') as file:
    dict_config = json.load(file)

token = dict_config['token']
path_file_ffmpef = Path(dict_config['path_file_ffmpef'])

queue_request_voice_tts = Jsonqueue.from_dict(dict_config['queue_request_voice_tts'])
bytessource_response_voice_tts = Bytessource.from_dict(dict_config['bytessource_response_voice_tts'])

queue_request_voice_authenticator = Jsonqueue.from_dict(dict_config['queue_request_voice_authenticator'])
bytessource_response_voice_authenticator = Bytessource.from_dict(dict_config['bytessource_response_voice_authenticator'])

bytessource_bot = Bytessource.from_dict(dict_config['bytessource_bot'])
bytessource_sound = bytessource_bot.join(['sound'])
bytessource_file = bytessource_bot.join(['file'])
bytessource_voice_sound = bytessource_bot.join(['voice_sound'])
bytessource_voice_encoding = bytessource_bot.join(['voice_encoding'])
bytessource_tts_output = bytessource_bot.join(['sound_tts'])

bytessource_log_event = bytessource_bot.join(['log','event'])
# client_tts = ClientBreakerAudioTts(queue_request_voice_tts)

client_auth = ClientVoiceAuthenticator(
    queue_request_voice_authenticator,
    bytessource_response_voice_authenticator)

bot = BotClone(
    token, 
    path_file_ffmpef,
    bytessource_bot)

bot.add_agent(AgentLoggerEvent(bytessource_log_event))

bot.add_command(CommandHelp())
bot.add_command(CommandJoin())
bot.add_command(CommandLeave())

bot.add_command(CommandAliasme())
bot.add_command(CommandAliaslist())

bot.add_command(CommandPlay(bytessource_sound))
bot.add_command(CommandPlaylist(bytessource_sound))

bot.add_command(CommandPost(bytessource_file))
bot.add_command(CommandPostlist(bytessource_file))

# bot.add_command(CommandTts(client_tts, bytessource_voice, bytessource_output_tts))
bot.add_command(CommandRecordme(client_auth, bytessource_voice_sound, bytessource_voice_encoding))
bot.add_command(CommandPlayme(bytessource_voice_sound))
bot.add_command(CommandPlayuser(bytessource_voice_sound))
bot.add_command(CommandVoiceauth(client_auth, bytessource_voice_sound, bytessource_voice_encoding))

bot.add_command(CommandLogplotevent())



# bot.add_command(CommandPlayalias(bytessource_sound))
bot.run()

