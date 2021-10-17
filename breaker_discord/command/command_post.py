from pathlib import Path

import discord

from breaker_discord.command.command import Command

class CommandPost(Command):

    def __init__(self, bytearraysource_files) -> None:
        self.bytearraysource_files = bytearraysource_files
        help_message = '!show \{filename\}'
        help_message += 'filename: the filename of an existing file to post\n'
        super().__init__('post', help_message)

    async def execute(self, list_argument, message) -> None:
        bytearraysource_file = self.bytearraysource_files.join([list_argument[0]]) 
        if bytearraysource_file.exists():
            filename = list_argument[0]
        else:
            list_list_key = self.bytearraysource_files.list_shallow(list_argument[0])
            if len(list_list_key) == 1:
                bytearraysource_file = self.bytearraysource_files.join(list_list_key[0])
                filename = list_list_key[0][0]
            else:
                await message.channel.send("no such file: " + str(list_argument[0]))
                return
                
        voice_client = message.guild.voice_client
        if not voice_client.is_connected():            
            await message.channel.send("The bot is not connected to a voice channel.")
            return

        await self.bot.post_bytearraysource(bytearraysource_file, filename, message.channel)

class CommandPostlist(Command):

    def __init__(self, bytearraysource_files) -> None:
        self.bytearraysource_files = bytearraysource_files
        help_message = '!postlist'
        help_message += 'list the available files !post\n'
        super().__init__('postlist', help_message)

    async def execute(self, list_argument, message) -> None:
        list_list_key = self.bytearraysource_files.list_shallow()
        
        list_message = 'Listing files  available:\n'
        for list_key in list_list_key:
            list_message += list_key[0] + '\n'
        await message.channel.send(list_message)
        
        #TODO convert the 