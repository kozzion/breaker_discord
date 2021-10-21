import json
import hashlib
import time

from breaker_core.tools_general import ToolsGeneral
from breaker_core.datasource.bytessource import Bytessource as Bytessource

from breaker_discord.command.command import Command
from breaker_discord.client.client_breaker_audio_tts import ClientBreakerAudioTts


class CommandMacroAdd(Command):
    
    def __init__(self) -> None:

        help_message = '\n'
        help_message += '!tts \{pipeline\} \{user_id\} "\{text\}"\n'
        help_message += '\{pipeline\} to process the request, currently support eng and cmn\n'
        help_message += '\{user_id\} to be used form whom the voice will be used\n'
        help_message += '\{text\} to transformed to speach\n'
        super().__init__('tts', help_message)
          

    async def execute(self, list_argument, message) -> None:
        server = message.guild
        voice_client = server.voice_client

        language_code_639_3 = list_argument[0]
        id_user = list_argument[1]
        text = list_argument[2]

        id_user = list_argument[0]
        if not ToolsGeneral.str_is_int(id_user):
            id_user = self.bot.state['dict_alias'][id_user]


