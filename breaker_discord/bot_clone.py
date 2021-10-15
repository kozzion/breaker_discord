import os
import json
import sys
import discord
import hashlib
import time

# from discord.ext import commands,tasks
from pathlib import Path

from breaker_discord.client_breaker_audio_tts import ClientBreakerAudioTts
from breaker_discord.extension.voice_client_extended import VoiceClientExtented
from breaker_discord.extension.reader import ConsumerLogger

from breaker_core.datasource.bytearraysource_generator import BytearraysourceGenerator

class BotClone:

    def __init__(
            self, 
            token:str, 
            path_file_ffmpeg:Path, 
            client_tts:ClientBreakerAudioTts,
            bytearraysource_generator_voice:BytearraysourceGenerator,
            bytearraysource_generator_output:BytearraysourceGenerator) -> None:
            
        self.path_file_state = Path('state.json')
        self.state = {}
        self.load_state()

        self.token = token
        self.path_file_ffmpeg = path_file_ffmpeg

        self.bytearraysource_generator_voice = bytearraysource_generator_voice
        self.bytearraysource_generator_output = bytearraysource_generator_output
        
        self.client_tts = client_tts
        # intents = discord.Intents().all() #TODO no idea what this does
        self.client_bot = discord.Client() #intents=intents)
        self.client_voice = None 
        self.consumer_logger = ConsumerLogger(self.client_bot)
        
        self.register_events()
        # self.register_commands()

    def load_state(self):
        if self.path_file_state.is_file():
            with self.path_file_state.open('r', encoding='utf-8') as file:
                self.state = json.load(file)
        if not 'dict_alias' in self.state:
            self.state['dict_alias'] = {}

    def save_state(self):
        with self.path_file_state.open('w', encoding='utf-8') as file:
            json.dump(self.state, file)

    def register_events(self):
        @self.client_bot.event
        async def on_ready():
            guild_count = 0
            for guild in self.client_bot.guilds:
                print(f"- {guild.id} (name: {guild.name})") #TODO is this id a string?
                guild_count = guild_count + 1
            print("SampleDiscordBot is in " + str(guild_count) + " guilds.")
            sys.stdout.flush()

            await self.join_channel_by_name('Kozzions secret castle','Voice')

        @self.client_bot.event
        async def on_message(message):
            if message.author.id != self.client_bot.user.id:
                if message.content == "hello":
                    await message.channel.send("hey meatsack")

                if message.content[0] == '!':
                    await self.handle_command(message)

    async def join_channel_by_name(self, name_guild, name_channel):
        for guild in self.client_bot.guilds:
            if guild.name == name_guild:
                for channel in guild.channels:
                    if channel.name == name_channel: 
                        await self.join_channel(channel)   
                       
    async def join_channel(self, channel):
        self.client_voice = await channel.connect(cls=VoiceClientExtented)
        self.client_voice.register_consumer(self.consumer_logger)
        self.consumer_logger.client_voice = self.client_voice

    def get_bytearraysource_voice(self, user_id:str):
        print(user_id)
        list_list_key = self.bytearraysource_generator_voice.list_for_prefix(['voice', user_id])
        if len(list_list_key) == 0:
            return None
        else:
            print('list_list_key')
            print(list_list_key)
            return self.bytearraysource_generator_voice.generate(list_list_key[0])
        # list_name_file = os.listdir(self.path_dir_voice)
        # for name_file in list_name_file:

        #     user_id_file = name_file.split('_')[0]
        #     print(user_id_file)
        #     print(user_id)
        #     print(type(user_id_file))
        #     print(type(user_id))
        #     sys.stdout.flush()
        #     if user_id_file == user_id:
        #         print('here')
        #         sys.stdout.flush()
        #         return self.path_dir_voice.joinpath(name_file)
        # return None



    #
    # Command section
    #

    def parse_command(self, message):
        str_message = message.content

        list_part_quote = str_message.split('"')

        if len(list_part_quote) == 1:
            list_part = list_part_quote[0].split(' ')
        else:
            list_part = list_part_quote[0].split(' ')
            list_part.append(list_part_quote[1])

        list_part_clean = []
        for part in list_part:
            part = part.strip()
            if 0 < len(part):
                list_part_clean.append(part)

        return list_part_clean[0][1:], list_part_clean[1:]

    async def handle_command(self, message):
        keyword, list_argument = self.parse_command(message)
        print(keyword)
        sys.stdout.flush()
        if keyword  == 'help':
            await self.command_help(list_argument, message)

        if keyword  == 'join':
            await self.command_join(list_argument, message)
        
        if keyword  == 'leave':
            await self.command_leave(list_argument, message)

        if keyword  == 'play':
            await self.command_play(list_argument, message)

        if keyword  == 'playme':
            await self.command_playme(list_argument, message)

        if keyword  == 'playuser':
            await self.command_playuser(list_argument, message)

        if keyword  == 'tts':
            await self.command_tts(list_argument, message)

        if keyword  == 'cloneme':
            await self.command_cloneme(list_argument, message)

        if keyword  == 'aliasme':
            await self.command_aliasme(list_argument, message)

        if keyword  == 'aliasme':
            await self.command_aliasme(list_argument, message)

        if keyword  == 'listalias':
            await self.command_listalias(list_argument, message)

        if keyword  == 'status':
            await self.command_status(list_argument, message)

    async def command_help(self, list_argument, message):
        message_text = ''
        message_text += '!help to show this help message\n'
        message_text += '!cloneme to clone your voice\n'
        message_text += '!aliasme to create an alias for your userid\n'
        message_text += '!listalias list all known aliasses\n'
        message_text += '!tts \{lang\} \{alias\} "\{text\}" to play a text to speach fragment\n'

        await message.channel.send(message_text)
 
    async def command_join(self, list_argument, message):
        if not message.author.voice:
            await message.channel.send("{} is not connected to a voice channel".format(message.author.name))
            return
        else:
            channel = message.author.voice.channel
        await self.join_channel(channel)


    async def command_leave(self, list_argument, message):
        voice_client = message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await message.channel.send("The bot is not connected to a voice channel.")



    @staticmethod
    def str_is_int(str_value:str):
        try:
            int(str_value)
            return True
        except ValueError:
            return False

    async def command_tts(self, list_argument, message):

        server = message.guild
        voice_client = server.voice_client

        async with message.channel.typing():
            
            language_code_639_3 = list_argument[0]
            id_user = list_argument[1]
            text = list_argument[2]
            if BotClone.str_is_int(id_user):
                bytearraysource_voice = self.get_bytearraysource_voice(id_user)
            elif id_user in self.state['dict_alias']:
                id_user = self.state['dict_alias'][id_user]
                bytearraysource_voice = self.get_bytearraysource_voice(id_user)
            else:
                await message.channel.send("No voice file for such file: " + id_user)
                return
            if bytearraysource_voice == None:
                await message.channel.send("No voice file for such file: " + id_user)
                return

            dict_request = {
                'language_code_639_3':language_code_639_3,
                'id_user':id_user,
                'text':text
            }
            hash_request = hashlib.md5(json.dumps(dict_request).encode('utf-8')).hexdigest()
            bytearraysource_output = self.bytearraysource_generator_output.generate([hash_request])

            sys.stdout.flush()
            self.client_tts.synthesize(language_code_639_3, bytearraysource_voice, text , bytearraysource_output)
            
            async with message.channel.typing():
    
                if not bytearraysource_output.exists():
                    await message.channel.send("Output missing") #TODO this is nonsense
                
                path_file_temp = 'temp.wav' #TODO make bytearray_source getable as tempfilepath
                with open(path_file_temp, 'wb') as file:
                    file.write(bytearraysource_output.load()) #TODO make bytearray_source getable as tempfilepath

                voice_client = message.guild.voice_client
                voice_client.play(discord.FFmpegPCMAudio(executable=self.path_file_ffmpeg, source=path_file_temp))
                #os.remove(path_file_temp) #TODO make bytearray_source getable as tempfilepath

  
    async def command_cloneme(self, list_argument, message):
        print('command_cloneme')
        id_user = str(message.author.id)
        if self.client_voice == None:
            await message.channel.send("Not connected to a channel")
        else:
            await message.channel.send("Cloning " + message.author.display_name + " or " + id_user)
        
        count_packet = 500
        if 0 < len(list_argument):
            count_packet = int(list_argument[0])

        str_timestamp = str(int(time.time())) + '.wav'
        self.consumer_logger.dict_id_user_to_bytearraysource[id_user] = self.bytearraysource_generator_voice.generate(['voice', id_user, str_timestamp])
        self.consumer_logger.dict_id_user_to_count_packet_desired[id_user] = count_packet
        self.consumer_logger.dict_id_user_to_count_packet_reported[id_user] = 0
        self.consumer_logger.dict_id_user_to_channel[id_user] = message.channel
        self.consumer_logger.dict_id_user_to_display_name[id_user] = message.author.display_name
        self.consumer_logger.dict_id_user_to_list_packet[id_user] = []

    async def command_aliasme(self, list_argument, message):
        print('command_aliasme')
        id_user = str(message.author.id)
        self.consumer_logger.dict_id_user_to_display_name[id_user] = message.author.display_name
        if 0 < len(list_argument):
            # self.create_alias(list_argument[0], str(id_user))
            self.state['dict_alias'][list_argument[0]] = id_user
            self.save_state()
            await message.channel.send("Created alias for: " + id_user + " as: "+ list_argument[0])

    async def command_play(self, list_argument, message):
        
        voice_client = message.guild.voice_client
        if voice_client.is_connected():
            async with message.channel.typing():
                path_file_audio = Path(list_argument[0])
                print(path_file_audio)
                if not path_file_audio.is_file():
                    await message.channel.send("no such file: " + str(path_file_audio))
                    
                voice_client.play(discord.FFmpegPCMAudio(executable=self.path_file_ffmpeg, source=path_file_audio))
            await message.channel.send('**Now playing:** {}'.format(path_file_audio))
        else:
            await message.channel.send("The bot is not connected to a voice channel.")

    async def command_playme(self, list_argument, message):
        print('command_playme')
        id_user = str(message.author.id)

        bytearraysource_voice = self.get_bytearraysource_voice(id_user)
        if bytearraysource_voice == None:
            await message.channel.send("No voice fragment for : " + message.author.display_name)
        elif not bytearraysource_voice.exists():
            await message.channel.send("No voice fragment for : " + message.author.display_name)
        else:
            path_file_temp = 'temp.wav' #TODO make bytearray_source getable as tempfilepath
            with open(path_file_temp, 'wb') as file:
                file.write(bytearraysource_voice.load()) #TODO make bytearray_source getable as tempfilepath

            voice_client = message.guild.voice_client
            voice_client.play(discord.FFmpegPCMAudio(executable=self.path_file_ffmpeg, source=path_file_temp))

    async def command_playuser(self, list_argument, message):
        print('command_playuser')
        id_user = list_argument[0]
        if BotClone.str_is_int(id_user):
            bytearraysource_voice = self.get_bytearraysource_voice(id_user)
        elif id_user in self.state['dict_alias']:
            bytearraysource_voice = self.get_bytearraysource_voice(self.state['dict_alias'][id_user])
        else:
            await message.channel.send("No voice fragment for : " + id_user)
            return

 
        if bytearraysource_voice == None:
            await message.channel.send("No voice fragment for : " + id_user)
        elif not bytearraysource_voice.exists():
            await message.channel.send("No voice fragment for : " + id_user)
        else:
            path_file_temp = 'temp.wav' #TODO make bytearray_source getable as tempfilepath
            with open(path_file_temp, 'wb') as file:
                file.write(bytearraysource_voice.load()) #TODO make bytearray_source getable as tempfilepath

            voice_client = message.guild.voice_client
            voice_client.play(discord.FFmpegPCMAudio(executable=self.path_file_ffmpeg, source=path_file_temp))
    
    async def command_listalias(self, list_argument, message):
        print('command_listalias')
        message_list_alias = 'listing known aliases\n'
        for id_user, alias in self.state['dict_alias'].items():
            message_list_alias += id_user + ' ' + alias + '\n' 
        await message.channel.send(message_list_alias)

    async def command_status(self, list_argument, message):
        message_status = ''
        await message.channel.send("'Status'")


  
    def run(self):
        self.client_bot.run(self.token)
