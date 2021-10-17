from io import BytesIO
import os
import json
import sys
import hashlib
import time
from pathlib import Path
from typing import BinaryIO

import discord

from breaker_core.tools_general import ToolsGeneral
from breaker_core.datasource.bytearraysource import Bytearraysource

from breaker_discord.extension.voice_client_extended import VoiceClientExtented
from breaker_discord.extension.reader import ConsumerLogger
from breaker_discord.extension.reader import ConsumerSplitter
from breaker_discord.extension.processor.processor_opus_track_speaker import ProcessorOpusTrackSpeaker

from breaker_discord.agent.agent import Agent
from breaker_discord.command.command import Command

class BotClone:

    def __init__(
            self, 
            token:str,
            path_file_ffmpeg:Path,
            bytearraysource_bot:Bytearraysource) -> None:
        self.token = token
        self.path_file_ffmpeg = path_file_ffmpeg
        self.bytearraysource_bot = bytearraysource_bot
        self.load_state()

        

        self.client_bot = discord.Client()
        self.client_voice = None 
        #self.consumer_logger = ConsumerLogger(self.client_bot)
        self.consumer = ConsumerSplitter(self.client_bot)
        self.register_events()
        # self.register_commands()
        self.dict_command = {}
        

    def load_state(self):
        bytearraysource_state = self.bytearraysource_bot.join(['state.json'])
        if bytearraysource_state.exists():
            self.state = json.loads(bytearraysource_state.read().decode('utf-8'))
            if not 'dict_alias' in self.state:
                self.state['dict_alias'] = {}
        else:
            self.state = {}
            self.state['dict_alias'] = {}
            self.save_state()
        
            
    def save_state(self):
        bytearraysource_state = self.bytearraysource_bot.join(['state.json'])
        bytearraysource_state.write(json.dumps(self.state).encode('utf-8'))

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
        async def on_member_join(member):
            print("Recognized that " + member.name + " joined")

        # @self.client_bot.event
        # async def on_voice_state_update(member, before, after):
        #     print('on_voice_state_update')
        #     print(member)
        #     print(before)
        #     print(after)
        #     sys.stdout.flush()
        #     if before.voice.voice_channel is None and after.voice.voice_channel is not None:
        #         for channel in before.server.channels:
        #             if channel.name == 'general':
        #                 await client.send_message(channel, "Howdy")

        @self.client_bot.event
        async def on_message(message):
            if message.author.id != self.client_bot.user.id:
                if message.content == "hello":
                    await message.channel.send("hey meatsack")

                if message.content[0] == '!':
                    await self.handle_command(message)

    def add_agent(self, agent:Agent):
        if agent.id_agent in self.dict_agent:
            raise Exception('duplicate agent: ' + agent.id_agent) 
        self.dict_agent[agent.id_agent] = agent
        agent.bot = self

    def add_command(self, command:Command):
        if command.keyword in self.dict_command:
            raise Exception('duplicate keyword: ' + command.keyword) 
        self.dict_command[command.keyword] = command
        command.bot = self
        
    async def join_channel_by_name(self, name_guild, name_channel):
        for guild in self.client_bot.guilds:
            if guild.name == name_guild:
                for channel in guild.channels:
                    if channel.name == name_channel: 
                        await self.join_channel(channel)   
                       
    async def join_channel(self, channel):
        self.client_voice = await channel.connect(cls=VoiceClientExtented)
        self.client_voice.register_consumer(self.consumer)
        self.consumer.client_voice = self.client_voice
        bytearraysource_conversation = self.bytearraysource_bot.join(['conversation'])
        self.consumer.register_processor_opus(ProcessorOpusTrackSpeaker(self.client_voice, bytearraysource_conversation))

    async def play_bytearraysource(self, bytearraysource_sound:Bytearraysource):
        path_file_temp = 'temp.wav' #TODO make bytearray_source getable as tempfilepath
        with open(path_file_temp, 'wb') as file:
            file.write(bytearraysource_sound.read()) #TODO make bytearray_source getable as tempfilepath
        self.client_voice.play(discord.FFmpegPCMAudio(executable=self.path_file_ffmpeg, source=path_file_temp))
        


    async def post_bytearraysource(self, bytearraysource_post:Bytearraysource, filename, channel):
        bytesio = BytesIO()
        bytesio.write(bytearraysource_post.read())
        bytesio.seek(0)
        discord_file = discord.File(bytesio, filename=filename)
        await channel.send(file=discord_file)    

    #
    # Command section
    #

    def parse_command(self, message):
        #TODO this can be a lot cleaner
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

        if keyword  == 'cloneme':
            await self.command_cloneme(list_argument, message)

        if keyword in self.dict_command:
            await self.dict_command[keyword].execute(list_argument, message)

        
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



  
    def run(self):
        self.client_bot.run(self.token)
