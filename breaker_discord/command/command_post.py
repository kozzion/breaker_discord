from pathlib import Path

import discord

from breaker_discord.command.command import Command

class CommandPost(Command):

    def __init__(self, bytessource_files) -> None:
        self.bytessource_files = bytessource_files
        help_message = '!show \{filename\}'
        help_message += 'filename: the filename of an existing file to post\n'
        super().__init__('post', help_message)

    async def execute(self, list_argument, message) -> None:
        if len(list_argument) == 0:       
            await message.channel.send("Please provide a \{filename\} argument.")   
            return
        bytessource_file = self.bytessource_files.join([list_argument[0]]) 
        if bytessource_file.exists():
            filename = list_argument[0]
        else:
            list_list_key = self.bytessource_files.list_shallow()
            list_can = []
            for list_key in list_list_key:
                if list_key[0].startswith(list_argument[0]) == 1:
                    list_can.append(list_key)

            if len(list_can) == 1:
                bytessource_file = self.bytessource_files.join(list_can[0])
                filename = list_can[0][-1]
            else:
                await message.channel.send("no such file: " + str(list_argument[0]))
                return

     
        voice_client = message.guild.voice_client
        if not voice_client.is_connected():            
            await message.channel.send("The bot is not connected to a voice channel.")
            return

        await self.bot.post_bytessource(bytessource_file, filename, message.channel)

class CommandPostlist(Command):

    def __init__(self, bytessource_files) -> None:
        self.bytessource_files = bytessource_files
        help_message = '!postlist'
        help_message += 'list the available files !post\n'
        super().__init__('postlist', help_message)

    async def execute(self, list_argument, message) -> None:
        list_list_key = self.bytessource_files.list_shallow()
        
        list_message = 'Listing files  available:\n'
        for list_key in list_list_key:
            list_message += list_key[0] + '\n'
        await message.channel.send(list_message)
        
        #TODO convert the 