from pathlib import Path

import discord

from breaker_discord.command.command import Command

class CommandPlay(Command):

    def __init__(self, bytessource_sounds) -> None:
        self.bytessource_sounds = bytessource_sounds
        help_message = '!play \{filename\} \{volume_factor\}'
        help_message += '\{filename\}: the filename of an existing audio file to play\n'
        help_message += '\{volume_factor\} (optional): override the default volume factor for playing the sound\n'
        super().__init__('play', help_message)

    async def execute(self, list_argument, message) -> None:
        if len(list_argument) == 0:       
            await message.channel.send("Please provide a \{filename\} argument.")   
            return

        bytessource_sound = self.bytessource_sounds.join([list_argument[0]])
        if not bytessource_sound.exists():
            list_list_key = self.bytessource_sounds.list_shallow()
            list_can = []
            for list_key in list_list_key:
                if list_key[0].startswith(list_argument[0]) == 1:
                    list_can.append(list_key)

            if len(list_can) == 1:
                bytessource_sound = self.bytessource_sounds.join(list_can[0])
            else:
                await message.channel.send("no such sound: " + str(list_argument[0]))
                return

        voice_client = message.guild.voice_client
        if not voice_client.is_connected():            
            await message.channel.send("The bot is not connected to a voice channel.")
            return
        if 1 < len(list_argument):
            volume_factor = float(list_argument[1])
            await self.bot.play_bytessource(bytessource_sound, volume_factor)
        else:
            await self.bot.play_bytessource(bytessource_sound)
        await message.channel.send('**Now playing:** {}'.format(list_argument[0]))

class CommandPlaylist(Command):

    def __init__(self, bytessource_sounds) -> None:
        self.bytessource_sounds = bytessource_sounds
        help_message = '!playlist'
        help_message += 'list the available audiofiles for !play\n'
        super().__init__('playlist', help_message)

    async def execute(self, list_argument, message) -> None:
        list_list_key = self.bytessource_sounds.list_shallow()
        
        list_message = 'Listing sound available:\n'
        for list_key in list_list_key:
            list_message += list_key[0] + '\n'
        await message.channel.send(list_message)

class CommandPlayvolume(Command):

    def __init__(self, bytessource_sounds) -> None:
        self.bytessource_sounds = bytessource_sounds
        help_message = '!playvolume {\volume_factor\}'
        help_message += '{\volume_factor\} sets the default volume factor for the audio player, initial value is 0.5\n'
        super().__init__('playlist', help_message)

    async def execute(self, list_argument, message) -> None:
        volume_factor = float(list_argument[0])
        self.bot.state['volume_factor'] = volume_factor
        self.bot.save_state()
        await message.channel.send('Volume factor set to :' + str(volume_factor))

class CommandSavesound(Command):
    def __init__(self, bytessource_sounds) -> None:
        self.bytessource_sounds = bytessource_sounds
        help_message = '!savesound \{url\}'
        help_message += 'list the availelble audiofiles for !playme\n'
        super().__init__('playlist', help_message)

    async def execute(self, list_argument, message) -> None:
        await message.channel.send('Not implemented')
        #TODO convert the 


# class CommandPlayalias(Command):

#     def __init__(self, bytessource_sounds) -> None:
#         self.bytessource_sounds = bytessource_sounds
#         help_message = '!playlist'
#         help_message += 'list the availelble audiofiles for !playme\n'
#         super().__init__('playlist', help_message)

#     async def execute(self, list_argument, message) -> None:
#         bytessource_sound = self.bytessource_sounds.generate([list_argument[0]])
#         list_list_key = bytessource_sound.list()
        
#         #TODO convert the 

