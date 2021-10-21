
import time

from breaker_discord.command.command import Command




class CommandCloneme(Command):

    def __init__(self, bytessource_voice_sound: Bytessource, bytessource_voice_encoding: Bytessource) -> None:
        self.bytessource_voice_sound = bytessource_voice_sound
        help_message = '!cloneme'
        help_message += '\{duration_frames\} (default=500): duration in frames for which the log should be shown\n'
        super().__init__('logplotevent', help_message, ['AgentLoggerEvent'])

    async def execute(self, list_argument, message) -> None:
        print('command_cloneme')

    def __init__(self, bytessource_voice_sound: Bytessource, bytessource_voice_encoding: Bytessource) -> None:
        self.bytessource_voice_sound = bytessource_voice_sound
class CommandAuthme(Command):

    def __init__(self, bytessource_voice) -> None:
        self.bytessource_voice = bytessource_voice
        help_message = '!authme \{duration_frames\}'
        help_message += '\{duration_frames\} (default=500): duration in frames for which the log should be shown\n'
        super().__init__('authme ', help_message)

    async def execute(self, list_argument, message) -> None:
        print('command_cloneme')
        id_user = str(message.author.id)
        if self.client_voice == None:
            await message.channel.send("Not connected to a channel")
        else:
            await message.channel.send("Cloning " + message.author.display_name + " or " + id_user)

        if 0 < len(list_argument):
            duration_frames = int(list_argument[0])
        else:
            duration_frames = 500
        
        if 0 < len(list_argument):
            count_packet = int(list_argument[0])

        str_timestamp = str(int(time.time()))
        self.bot.consumer_logger.dict_id_user_to_bytessource[id_user] = self.bytessource_voice.join(['voice', id_user, str_timestamp])
        self.bot.consumer_logger.dict_id_user_to_count_packet_desired[id_user] = duration_frames
        self.bot.consumer_logger.dict_id_user_to_count_packet_reported[id_user] = 0
        self.bot.consumer_logger.dict_id_user_to_channel[id_user] = message.channel
        self.bot.consumer_logger.dict_id_user_to_display_name[id_user] = message.author.display_name
        self.bot.consumer_logger.dict_id_user_to_list_packet[id_user] = []
