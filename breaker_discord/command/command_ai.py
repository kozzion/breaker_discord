import json
import hashlib
import time

from breaker_core.tools_general import ToolsGeneral
from breaker_core.datasource.bytessource import Bytessource
from breaker_core.datasource.bytessource_bytearray import BytessourceBytearray
from breaker_discord.command.command import Command
from breaker_discord.client.client_voice_synthesizer import ClientVoiceSynthesizer
from breaker_discord.client.client_voice_authenticator import ClientVoiceAuthenticator

class CommandTts(Command):
    
    def __init__(self, 
        client_tts:ClientVoiceSynthesizer,
        bytessource_voice:Bytessource,
        bytessource_output:Bytessource) -> None:
        self.client_tts = client_tts
        self.bytessource_voice = bytessource_voice
        self.bytessource_output = bytessource_output
        help_message = '\n'
        help_message += '!tts \{pipeline\} \{user_id\} "\{text\}"\n'
        help_message += 'pipeline to process the request, currently support eng and cmn\n'
        help_message += 'user_id to be used form whom the voice will be used\n'
        help_message += 'text to transformed to speach\n'
        super().__init__('tts', help_message)
          

    async def execute(self, list_argument, message) -> None:
        language_code_639_3 = list_argument[0]
        id_user = list_argument[1]
        text = list_argument[2]

        if not ToolsGeneral.str_is_int(id_user):
            if id_user in  self.bot.state['dict_alias']:
                id_user = self.bot.state['dict_alias'][id_user]
            else:
                await message.channel.send("Unknown id_user or alias: " + id_user)
                return

        
        bytessource_voice = ToolsCommandAi.get_bytessource_voice(self.bytessource_voice, id_user)
        if bytessource_voice is None:
                await message.channel.send("No voice segment recorded recorded id_user or alias: " + id_user)
                return
        response, bytessource_output = self.client_tts.synthesize(language_code_639_3, bytessource_voice, text)

        if not bytessource_output.exists():
            await message.channel.send("Output missing") #TODO this is nonsense
            return
        
        await self.bot.play_bytessource(bytessource_output)
            
class CommandRecordme(Command):

    def __init__(self, 
            client_voice_authenticator:ClientVoiceAuthenticator,
            bytessource_voice_sound: Bytessource, 
            bytessource_voice_encoding: Bytessource) -> None:
        self.client_voice_authenticator = client_voice_authenticator
        self.bytessource_voice_sound = bytessource_voice_sound
        self.bytessource_voice_encoding = bytessource_voice_encoding
        help_message = '\n'
        help_message += '!recordme \{duration_frames\}'
        help_message += 'records the user and generates an encoding from the recording'
        help_message += '\{duration_frames\} (default=200): duration in frames for which the recording should last\n'
        super().__init__('recordme', help_message)

    async def execute(self, list_argument, message) -> None:
        id_user = str(message.author.id)
        if self.bot.client_voice == None:
            await message.channel.send("Not connected to a channel")
        else:
            await message.channel.send("Recording " + message.author.display_name + " or " + id_user)

        if 0 < len(list_argument):
            duration_frames = int(list_argument[0])
        else:
            duration_frames = 200
        

        str_timestamp = str(int(time.time()))
        self.bot.consumer.dict_id_user_to_bytessource_sound[id_user] = self.bytessource_voice_sound.join([id_user, str_timestamp])
        self.bot.consumer.dict_id_user_to_bytessource_encoding[id_user] = self.bytessource_voice_encoding.join([id_user, str_timestamp])
        self.bot.consumer.dict_id_user_to_bytessource_encoding_dir[id_user] = ''
        self.bot.consumer.dict_id_user_to_client_encoding[id_user] = self.client_voice_authenticator
        self.bot.consumer.dict_id_user_to_bot[id_user] = self.bot
        self.bot.consumer.dict_id_user_to_count_packet_desired[id_user] = duration_frames
        self.bot.consumer.dict_id_user_to_count_packet_reported[id_user] = 0
        self.bot.consumer.dict_id_user_to_channel[id_user] = message.channel
        self.bot.consumer.dict_id_user_to_display_name[id_user] = message.author.display_name
        self.bot.consumer.dict_id_user_to_list_packet[id_user] = []

class CommandVoiceauth(Command):

    def __init__(self, 
            client_voice_authenticator:ClientVoiceAuthenticator,
            bytessource_voice_sound: Bytessource, 
            bytessource_voice_encoding: Bytessource) -> None:
        self.client_voice_authenticator = client_voice_authenticator
        self.bytessource_voice_sound = bytessource_voice_sound
        self.bytessource_voice_encoding = bytessource_voice_encoding
        help_message = '\n'
        help_message += '!voiceauth \{id_user\} \{duration_frames\}'
        help_message += 'records the user and tries to authenticate the user as the id_user given'
        help_message += '\{id_user\}: id_user of the user the requester wants to be authenticated at\n'
        help_message += '\{duration_frames\} (default=200): duration in frames for which the recording should last\n'
        super().__init__('voiceauth', help_message)

    async def execute(self, list_argument, message) -> None:
        print('command_voiceauth')
        id_user = str(message.author.id)
     
        if len(list_argument) == 0:
            await message.channel.send("must provide a id_user to authenticate as")
            return

        if self.bot.client_voice == None:
            await message.channel.send("Not connected to a channel")
            return
   

        id_user_as = list_argument[0]

        if 1 < len(list_argument):
            duration_frames = int(list_argument[1])
        else:
            duration_frames = 200
        
        await message.channel.send("Authentication " + message.author.display_name + " as " + id_user_as)

        str_timestamp = str(int(time.time()))
        self.bot.consumer.dict_id_user_to_bytessource_sound[id_user] = self.bytessource_voice_sound.join([id_user, str_timestamp])
        self.bot.consumer.dict_id_user_to_bytessource_encoding[id_user] = ''
        self.bot.consumer.dict_id_user_to_bytessource_encoding_dir[id_user] = self.bytessource_voice_encoding.join([id_user_as])
        self.bot.consumer.dict_id_user_to_client_encoding[id_user] = self.client_voice_authenticator
        self.bot.consumer.dict_id_user_to_bot[id_user] = self.bot
        self.bot.consumer.dict_id_user_to_count_packet_desired[id_user] = duration_frames
        self.bot.consumer.dict_id_user_to_count_packet_reported[id_user] = 0
        self.bot.consumer.dict_id_user_to_channel[id_user] = message.channel
        self.bot.consumer.dict_id_user_to_display_name[id_user] = message.author.display_name
        self.bot.consumer.dict_id_user_to_list_packet[id_user] = []

    @staticmethod
    async def plot_report(bot, channel, authentication_report) -> None:
        import matplotlib.pyplot as plt 
        plt.figure()
        plt.hist(authentication_report['authentication_report']['list_val_a_b'], bins=20)
        plt.hist(authentication_report['authentication_report']['list_val_b_b'], bins=20)
        plt.title('similarity')
        plt.ylabel('count')
        plt.xlabel('similarity')
        plt.legend(['attempt', 'reference'])
        path_file_plot = 'plot.png' #TODO make bytearray_source getable as tempfilepath
        plt.savefig(path_file_plot)
        with open(path_file_plot, 'rb') as file:
             #TODO make bytearray_source getable as tempfilepath
            bytessource_post = BytessourceBytearray(file.read())
        await bot.post_bytessource(bytessource_post, path_file_plot, channel)

class CommandPlayme(Command):
    
    def __init__(self, 
        bytessource_voice:Bytessource) -> None:
        self.bytessource_voice = bytessource_voice
        help_message = '\n'
        help_message += '!playme\n'
        help_message += 'play the most recent voice fragment recorded for the user\n'
        super().__init__('playme', help_message)
          
    async def execute(self, list_argument, message)-> None:
        print('command_playme')
        id_user = str(message.author.id)

        bytessource_voice = ToolsCommandAi.get_bytessource_voice(self.bytessource_voice, id_user)
        if bytessource_voice == None:
            await message.channel.send("No voice fragment for : " + message.author.display_name)
        elif not bytessource_voice.exists():
            await message.channel.send("No voice fragment for : " + message.author.display_name)
        else:
            await self.bot.play_bytessource(bytessource_voice)

class CommandPlayuser(Command):
    
    def __init__(self, 
        bytessource_voice:Bytessource) -> None:
        self.bytessource_voice = bytessource_voice
        help_message = '\n'
        help_message += '!playuser \{id_user\}\n'
        help_message += 'play the most recent voice fragment recorded for a user\n'
        help_message += '\{id_user\} the userid or alias of the user to play\n'
        
        super().__init__('playuser', help_message)

    async def execute(self, list_argument, message):
        id_user = list_argument[0]
        if not ToolsGeneral.str_is_int(id_user):
            id_user = self.bot.state['dict_alias'][id_user]
            
        bytessource_voice = ToolsCommandAi.get_bytessource_voice(self.bytessource_voice, id_user)

 
        if bytessource_voice == None:
            await message.channel.send("No voice fragment for : " + id_user)
        elif not bytessource_voice.exists():
            await message.channel.send("No voice fragment for : " + id_user) #TODO this should not happen
        else:
            await self.bot.play_bytessource(bytessource_voice)


class ToolsCommandAi:

    @staticmethod
    def get_bytessource_voice(bytessource_voice:Bytessource, user_id:str):
        return bytessource_voice.join([user_id]).join_last()
