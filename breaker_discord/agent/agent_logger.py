import sys
import time
import json

from breaker_core.datasource.bytessource import Bytessource
from breaker_discord.agent.agent import Agent

class AgentLoggerEvent(Agent):

    def __init__(self, bytessource_logger_events:Bytessource) -> None:
        super().__init__('AgentLoggerEvent')
        self.bytessource_logger_events = bytessource_logger_events
        self.client_discord = None


    def register_events(self, client_discord):
        self.client_discord = client_discord

        @self.client_discord.event
        async def on_voice_state_update(user, before, after):
     
            if (not before.channel is None) and (not after.channel is None) and (before.channel.id == after.channel.id):
                # only_log channel changes for now
                return

            if before.channel is None:
                id_channel_before = ''
            else:
                id_channel_before = str(before.channel.id)
            
            if after.channel is None:
                id_channel_after = ''
            else:
                id_channel_after  = str(after.channel.id)
            
            dict_event_update = {}
            dict_event_update['type_event'] = 'on_voice_state_update'
            dict_event_update['timestamp'] = int(time.time())
            dict_event_update['id_user'] = user.id
            dict_event_update['id_channel_before'] = id_channel_before
            dict_event_update['id_channel_after'] = id_channel_after

            self._log_event(dict_event_update)

    def _log_event(self, dict_event) -> None:
        bytessource_last = self._get_bytessource_last()
        dict_last = bytessource_last.read_json()
        dict_last['list_event'].append(dict_event)
        bytessource_last.write_json(dict_last)

    def _get_bytessource_last(self) -> 'Bytessource':
        bytessource_logger_last = self.bytessource_logger_events.join_last()
        if bytessource_logger_last is None: # TODO check if over max size
            str_timestamp = str(int(time.time()))
            bytessource_logger_last = self.bytessource_logger_events.join([str_timestamp])
            bytessource_logger_last.write_json({'list_event':[]})
            # create new logger object
        return bytessource_logger_last

    def querry_log(self, *, timestamp_start=None, timestamp_end=None, id_channel=None, list_id_user=None) -> 'list':
        #TODO ignore logs that are too old

        list_list_key = self.bytessource_logger_events.list_shallow()
        list_event = []
        for list_key in list_list_key:
            list_event.extend(self.bytessource_logger_events.join(list_key).read_json()['list_event'])

        list_event_sorted = sorted(list_event, key=lambda d: int(d['timestamp'])) 
        return list_event_sorted