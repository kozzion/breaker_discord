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
from breaker_core.datasource.bytessource import Bytessource

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
            bytessource_bot:Bytessource) -> None:
        self.token = token
        self.path_file_ffmpeg = path_file_ffmpeg
        self.bytessource_bot = bytessource_bot
        self.load_state()

        

        self.client_bot = discord.Client()
        self.client_voice = None 
        self.consumer = ConsumerLogger(self.client_bot)
        #self.consumer = ConsumerSplitter(self.client_bot)
        self.register_events()

        self.dict_command = {}
        self.dict_agent = {}
        

    def load_state(self):
        bytessource_state = self.bytessource_bot.join(['state.json'])
        if bytessource_state.exists():
            self.state = json.loads(bytessource_state.read().decode('utf-8'))
            if not 'dict_alias' in self.state:
                self.state['dict_alias'] = {}
            if not 'volume_factor' in self.state:
                self.state['volume_factor'] = 0.5
        else:
            self.state = {}
            self.state['dict_alias'] = {}
            self.state['volume_factor'] = 0.5
            self.save_state()
        
            
    def save_state(self):
        bytessource_state = self.bytessource_bot.join(['state.json'])
        bytessource_state.write(json.dumps(self.state).encode('utf-8'))

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
                if message.content[0] == '!':
                    await self.handle_command(message)

    def add_agent(self, agent:Agent):
        if agent.id_agent in self.dict_agent:
            raise Exception('duplicate agent: ' + agent.id_agent) 


        self.dict_agent[agent.id_agent] = agent
        agent.register_events(self.client_bot)

    def add_command(self, command:Command):
        if command.keyword in self.dict_command:
            raise Exception('duplicate keyword: ' + command.keyword)
        for id_agent_required in command.list_id_agent_required:
            if not id_agent_required in self.dict_agent:
                raise Exception('missing required agent: ' + id_agent_required) 
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
        bytessource_conversation = self.bytessource_bot.join(['conversation'])
        #TODO add this back
        #self.consumer.register_processor_opus(ProcessorOpusTrackSpeaker(self.client_voice, bytessource_conversation))

    async def play_bytessource(self, bytessource_sound:Bytessource, volume_factor:float=None):
        if volume_factor is None:
            volume_factor = self.state['volume_factor']
        path_file_temp = 'temp.wav' #TODO make bytearray_source getable as tempfilepath
        with open(path_file_temp, 'wb') as file:
            file.write(bytessource_sound.read()) #TODO make bytearray_source getable as tempfilepath
  
        str_volume = "{:.2f}".format(volume_factor)
        self.client_voice.play(discord.FFmpegPCMAudio(executable=self.path_file_ffmpeg, source=path_file_temp, options='-filter:a volume=' + str_volume))
    
    async def post_bytessource(self, bytessource_post:Bytessource, filename, channel):
        bytesio = BytesIO()
        bytesio.write(bytessource_post.read())
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

        if keyword in self.dict_command:
            try:
                await self.dict_command[keyword].execute(list_argument, message)
            except Exception as e:
                await message.channel.send("Exception while execution command: " + keyword)
                await message.channel.send(str(e))
                raise(e)
        else:
            await message.channel.send("Unknown command: " + keyword)

        



  
    def run(self):
        self.client_bot.run(self.token)
