from pathlib import Path

import discord

from breaker_discord.command.command import Command

class CommandPlay(Command):

    def __init__(self, bytearraysource_sounds) -> None:
        self.bytearraysource_sounds = bytearraysource_sounds
        help_message = '!play \{filename\}'
        help_message += 'filename: the filename of an existing audio file to play\n'
        super().__init__('play', help_message)

    async def execute(self, list_argument, message) -> None:
        bytearraysource_sound = self.bytearraysource_sounds.generate([list_argument[0]])
        if not bytearraysource_sound.exists():
            await message.channel.send("no such sound: " + str(list_argument[0]))
            return
            
        voice_client = message.guild.voice_client
        if not voice_client.is_connected():            
            await message.channel.send("The bot is not connected to a voice channel.")
            return

        await self.bot.play_bytearraysource(bytearraysource_sound)
        await message.channel.send('**Now playing:** {}'.format(list_argument[0]))

class CommandPlaylist(Command):

    def __init__(self, bytearraysource_sounds) -> None:
        self.bytearraysource_sounds = bytearraysource_sounds
        help_message = '!playlist'
        help_message += 'list the available audiofiles for !play\n'
        super().__init__('playlist', help_message)

    async def execute(self, list_argument, message) -> None:
        list_list_key = self.bytearraysource_sounds.list_shallow()
        
        list_message = 'Listing sound available:\n'
        for list_key in list_list_key:
            list_message += list_key[0] + '\n'
        await message.channel.send(list_message)


class CommandSavesound(Command):
    def __init__(self, bytearraysource_sounds) -> None:
        self.bytearraysource_sounds = bytearraysource_sounds
        help_message = '!savesound \{url\}'
        help_message += 'list the availelble audiofiles for !playme\n'
        super().__init__('playlist', help_message)

    async def execute(self, list_argument, message) -> None:
        await message.channel.send('Not implemented')
        #TODO convert the 


# class CommandPlayalias(Command):

#     def __init__(self, bytearraysource_sounds) -> None:
#         self.bytearraysource_sounds = bytearraysource_sounds
#         help_message = '!playlist'
#         help_message += 'list the availelble audiofiles for !playme\n'
#         super().__init__('playlist', help_message)

#     async def execute(self, list_argument, message) -> None:
#         bytearraysource_sound = self.bytearraysource_sounds.generate([list_argument[0]])
#         list_list_key = bytearraysource_sound.list()
        
#         #TODO convert the 

