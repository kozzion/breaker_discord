from os import name
from pathlib import Path
import tempfile

import matplotlib.pyplot as plt
import discord
import numpy as np

from breaker_discord.command.command import Command
from breaker_core.datasource.bytessource_bytearray import BytessourceBytearray

class CommandLogplotevent(Command):

    def __init__(self) -> None:
        help_message = '!logplotevent \{duration_m\}'
        help_message += '\{duration_m\} (default=60): duration in minutes for which the log should be shown\n'
        super().__init__('logplotevent', help_message, ['AgentLoggerEvent'])

    async def execute(self, list_argument, message) -> None:
        if 0 < len(list_argument):
            durantion_m = int(list_argument[0])
        else:
            durantion_m = 60

        agent_logger = self.bot.dict_agent['AgentLoggerEvent']
        list_event = agent_logger.querry_log()
        timestamp_first = list_event[0]['timestamp']
        timestamp_last = list_event[-1]['timestamp']

        dict_id_user_to_list_timestamp = {}
        dict_id_user_to_list_is_present = {}
        for event in list_event:
            
            id_user = str(event['id_user'])
            if id_user == str(self.bot.client_bot.user.id):
                continue # skip the bot events
            timestamp = event['timestamp'] 
            id_channel_before = event['id_channel_before']
            id_channel_after = event['id_channel_after']
            if not id_user in dict_id_user_to_list_timestamp:
                dict_id_user_to_list_timestamp[id_user] = []
                dict_id_user_to_list_is_present[id_user] = []
                if timestamp != timestamp_first:
                    dict_id_user_to_list_timestamp[id_user].append(timestamp_first)
                    if id_channel_before == '':
                        dict_id_user_to_list_is_present[id_user].append(0)
                    else:
                        dict_id_user_to_list_is_present[id_user].append(1)
                        
            dict_id_user_to_list_timestamp[id_user].append(timestamp)
            if id_channel_before== '':
                dict_id_user_to_list_is_present[id_user].append(0)
            else:
                dict_id_user_to_list_is_present[id_user].append(1)

            dict_id_user_to_list_timestamp[id_user].append(timestamp)
            if id_channel_after == '':
                dict_id_user_to_list_is_present[id_user].append(0)
            else:
                dict_id_user_to_list_is_present[id_user].append(1)

        for id_user in dict_id_user_to_list_timestamp:
            dict_id_user_to_list_timestamp[id_user].append(timestamp_last)
            dict_id_user_to_list_is_present[id_user].append(dict_id_user_to_list_is_present[id_user][-1])

        plt.figure()
        list_id_user = list(dict_id_user_to_list_timestamp.keys())
        print(list_id_user)
        for i, id_user in enumerate(list_id_user):
            print(id_user)
            print(self.bot.state['dict_alias'])
            name_user = id_user
            for alias, id_user_alias in self.bot.state['dict_alias'].items():
                if id_user_alias == id_user:
                    name_user = alias
                    break
            plt.subplot(len(list_id_user), 1, i+1)
            plt.title(name_user)
            array_timestamp = (np.array(dict_id_user_to_list_timestamp[id_user])  - timestamp_last)/ 3600
            plt.plot(array_timestamp, dict_id_user_to_list_is_present[id_user], label=name_user)

        with tempfile.TemporaryFile(suffix=".png") as file:
            plt.savefig(file, format="png")
            bytessource_post = BytessourceBytearray(file.read())
            await self.bot.post_bytessource(bytessource_post, 'plot.png', message.channel)

