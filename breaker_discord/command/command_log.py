from pathlib import Path

import discord

from breaker_discord.command.command import Command

class CommandLogprin(Command):

    def __init__(self, bytearraysource_sounds) -> None:
        self.bytearraysource_sounds = bytearraysource_sounds
        help_message = '!logprint \{duration_m\}'
        help_message += 'duration_m (default=60): duration in the log that should be shown\n'
        super().__init__('logprint', help_message)

    async def execute(self, list_argument, message) -> None:
        if 0 < len(list_argument):
            durantion_m = int(list_argument[0])
        else:
            durantion_m = 60
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