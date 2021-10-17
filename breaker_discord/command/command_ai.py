import json
import hashlib

from breaker_core.tools_general import ToolsGeneral
from breaker_core.datasource.bytearraysource import Bytearraysource

from breaker_discord.command.command import Command
from breaker_discord.client.client_breaker_audio_tts import ClientBreakerAudioTts

class CommandTts(Command):
    
    def __init__(self, 
        client_tts:ClientBreakerAudioTts,
        bytearraysource_voice:Bytearraysource,
        bytearraysource_output:Bytearraysource) -> None:
        self.client_tts = client_tts
        self.bytearraysource_voice = bytearraysource_voice
        self.bytearraysource_output = bytearraysource_output
        help_message = '!tts \{pipeline\} \{user_id\} "\{text\}"\n'
        help_message += 'pipeline to process the request, currently support eng and cmn\n'
        help_message += 'user_id to be used form whom the voice will be used\n'
        help_message += 'text to transformed to speach\n'
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
        bytearraysource_voice = ToolsCommandAi.get_bytearraysource_voice(self.bytearraysource_voice, id_user)



        dict_request = {
            'language_code_639_3':language_code_639_3,
            'id_user':id_user,
            'text':text
        }
        hash_request = hashlib.md5(json.dumps(dict_request).encode('utf-8')).hexdigest()
        bytearraysource_output = self.bytearraysource_output.generate([hash_request])

        self.client_tts.synthesize(language_code_639_3, bytearraysource_voice, text , bytearraysource_output)
        

        if not bytearraysource_output.exists():
            await message.channel.send("Output missing") #TODO this is nonsense
            return
        
        await self.bot.play_bytearraysource(bytearraysource_voice)
            
  
class CommandPlayme(Command):
    
    def __init__(self, 
        bytearraysource_voice:Bytearraysource) -> None:
        self.bytearraysource_voice = bytearraysource_voice
        help_message = '!playme\n'
        help_message += 'play the most recent voice fragment recorded for the user\n'
        super().__init__('playme', help_message)
          
    async def execute(self, list_argument, message)-> None:
        print('command_playme')
        id_user = str(message.author.id)

        bytearraysource_voice = ToolsCommandAi.get_bytearraysource_voice(self.bytearraysource_voice, id_user)
        if bytearraysource_voice == None:
            await message.channel.send("No voice fragment for : " + message.author.display_name)
        elif not bytearraysource_voice.exists():
            await message.channel.send("No voice fragment for : " + message.author.display_name)
        else:
            await self.bot.play_bytearraysource(bytearraysource_voice)

class CommandPlayuser(Command):
    
    def __init__(self, 
        bytearraysource_voice:Bytearraysource) -> None:
        self.bytearraysource_voice = bytearraysource_voice
        help_message = '!playuser\n'
        help_message += 'play the most recent voice fragment recorded for a user\n'
        super().__init__('playuser', help_message)

    async def execute(self, list_argument, message):
        id_user = list_argument[0]
        if not ToolsGeneral.str_is_int(id_user):
            id_user = self.bot.state['dict_alias'][id_user]
        bytearraysource_voice = ToolsCommandAi.get_bytearraysource_voice(self.bytearraysource_voice, id_user)

 
        if bytearraysource_voice == None:
            await message.channel.send("No voice fragment for : " + id_user)
        elif not bytearraysource_voice.exists():
            await message.channel.send("No voice fragment for : " + id_user) #TODO this should not happen
        else:
            await self.bot.play_bytearraysource(bytearraysource_voice)


class ToolsCommandAi:

    @staticmethod
    def get_bytearraysource_voice(bytearraysource_voice:Bytearraysource, user_id:str):
        list_list_key = bytearraysource_voice.list_for_prefix([user_id])
        if len(list_list_key) == 0:
            return None
        else:
            return bytearraysource_voice.generate(list_list_key[0])
