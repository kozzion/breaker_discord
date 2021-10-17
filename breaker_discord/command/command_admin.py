import discord

from breaker_discord.command.command import Command

class CommandJoin(Command):
    
    def __init__(self) -> None:
        help_message = '!join\n'
        help_message += 'make the bot join the voice channel of the user giving the command\n'
        super().__init__('join', help_message)
    

    async def execute(self, list_argument, message) -> None:
        if not message.author.voice:
            await message.channel.send(message.author.name + " is not connected to a voice channel")
            return
        else:
            channel = message.author.voice.channel
        await self.bot.join_channel(channel)

class CommandLeave(Command):
    
    def __init__(self) -> None:
        help_message = '!leave\n'
        help_message += 'make the bot leave its current voice channel\n'
        super().__init__('leave', help_message)
    

    async def execute(self, list_argument, message) -> None:
        voice_client = message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await message.channel.send("The bot is not connected to a voice channel.")

class CommandHelp(Command):

    def __init__(self) -> None:
        help_message = '!help \{command\}\n'
        help_message += 'command: the command on which you want help, leave empty for a list of commands\n'
        super().__init__('help', help_message)
        

    async def execute(self, list_argument, message) -> None:
        if len(list_argument) == 0:
            help_message = ''
            help_message += 'A list of availeble commands:\n'
            for keyword in self.bot.dict_command:
                help_message += '!' + keyword + ' '
            await message.channel.send(help_message)
        else:
            keyword = list_argument[0]
            if keyword in self.bot.dict_command:
                await message.channel.send(self.bot.dict_command[keyword].help_message)
            else:
                await message.channel.send('No such command: ' + keyword)

class CommandAliasme(Command):
    def __init__(self) -> None:
        help_message = '!aliasme\n'
        help_message += 'Create an alias for the user that can serve as an alternative to as user_id\n'
        super().__init__('aliasme', help_message)
        

    async def execute(self, list_argument, message) -> None:
        print('execute')
        id_user = str(message.author.id)
        if 0 < len(list_argument):
            self.bot.state['dict_alias'][list_argument[0]] = id_user
            self.bot.save_state()
            await message.channel.send("Created alias for: " + id_user + " as: "+ list_argument[0])


class CommandAliaslist(Command):
    def __init__(self) -> None:
        help_message = '!aliaslist\n'
        help_message += 'List all aliasses for users\n'
        super().__init__('aliaslist', help_message)
        

    async def execute(self, list_argument, message) -> None:
        message_list_alias = 'listing known aliases\n'
        for id_user, alias in self.bot.state['dict_alias'].items():
            message_list_alias += id_user + ' ' + alias + '\n' 
        await message.channel.send(message_list_alias)