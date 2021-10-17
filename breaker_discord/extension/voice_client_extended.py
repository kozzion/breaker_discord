import sys
import threading

import discord

from breaker_discord.extension.reader import OpusEventAudioReader
from breaker_discord.extension.reader import ConsumerAudio

class VoiceClientExtented(discord.VoiceClient):
    def __init__(self, client, channel):
        super().__init__(client, channel)

        self._connecting = threading.Condition()
        self._reader = None
        self._ssrc_to_id = {}
        self._id_to_ssrc = {}
        self.websocket = None


    async def connect_websocket(self):
        # interception messages
        self.websocket = await discord.gateway.DiscordVoiceWebSocket.from_client(self)
        self.received_message_org = self.websocket.received_message
        self.websocket.received_message = self.received_message_intercept

        #complete connection
        self._connected.clear()
        while self.websocket.secret_key is None:
            await self.websocket.poll_event()
        self._connected.set()
        return self.websocket

    async def received_message_intercept(self, message):
        op = message['op']
        data = message['d']
        if op == discord.gateway.DiscordVoiceWebSocket.SESSION_DESCRIPTION:
            pass #await _do_hacks(self)

        elif op == discord.gateway.DiscordVoiceWebSocket.SPEAKING:
            user_id = str(data['user_id'])
            ssrc = str(data['ssrc'])
            self._add_ssrc(user_id, ssrc)

            # if self.guild:
            #     user = self.guild.get_member(user_id)
            # else:
            #     user = self._state.get_user(user_id)
            # self._state.dispatch('speaking_update', user, data['speaking'])

        elif op == discord.gateway.DiscordVoiceWebSocket.CLIENT_CONNECT:
            user_id = str(data['user_id'])
            ssrc = str(data['ssrc'])
            self._add_ssrc(user_id, ssrc)
        elif op == discord.gateway.DiscordVoiceWebSocket.SPEAKING:
            user_id = str(data['user_id'])
            self._remove_ssrc(user_id=user_id)
        else:
            print(message)
        return await self.received_message_org(message)

    async def on_voice_state_update(self, data):
        await super().on_voice_state_update(data)

        channel_id = str(data['channel_id'])
        guild_id = str(data['guild_id'])
        user_id = str(data['user_id'])

        if channel_id and channel_id != str(self.channel.id) and self._reader:
            # someone moved channels
            if str(self._connection.user.id) == user_id:
                # we moved channels
                # print("Resetting all decoders")
                self._reader._reset_decoders()

            # TODO: figure out how to check if either old/new channel
            #       is ours so we don't go around resetting decoders
            #       for irrelevant channel moving

            else:
                # someone else moved channels
                # print(f"ws: Attempting to reset decoder for {user_id}")
                ssrc, _ = self._get_ssrc_mapping(user_id=user_id)
                self._reader._reset_decoders(ssrc)

    # async def on_voice_server_update(self, data):
    #     await super().on_voice_server_update(data)
    #     ...


    def cleanup(self):
        super().cleanup()
        self.stop()

    # TODO: copy over new functions
    # add/remove/get ssrc

    def _add_ssrc(self, user_id:str, ssrc:str):
        if not isinstance(user_id, str):
            raise Exception()
        if not isinstance(ssrc, str):
            raise Exception()
        self._ssrc_to_id[ssrc] = user_id
        self._id_to_ssrc[user_id] = ssrc

    def _remove_ssrc(self, *, user_id:str):
        if not isinstance(user_id, str):
            raise Exception()
        ssrc = self._id_to_ssrc.pop(user_id, None)
        if ssrc:
            self._ssrc_to_id.pop(ssrc, None)

    def _get_ssrc_mapping(self, *, ssrc:str): #TODO this is not used correctly 
        if not isinstance(ssrc, str):
            raise Exception()
        user_id = self._ssrc_to_id.get(ssrc)
        return ssrc, user_id

    def register_consumer(self, consumer:ConsumerAudio):
   
        if not self.is_connected():
            raise RuntimeError('Not connected to voice.')

        # if not isinstance(sink, AudioSink):
        #     raise TypeError('sink must be an AudioSink not {0.__class__.__name__}'.format(sink))

        if self.is_listening():
            raise RuntimeError('Already receiving audio.')

        self._reader = OpusEventAudioReader(consumer, self)
        self._reader.start()

    def is_listening(self):
        """Indicates if we're currently receiving audio."""
        return self._reader is not None and self._reader.is_listening()

    def stop_listening(self):
        """Stops receiving audio."""
        if self._reader:
            self._reader.stop()
            self._reader = None

    def stop_playing(self):
        """Stops playing audio."""
        if self._player:
            self._player.stop()
            self._player = None

    def stop(self):
        """Stops playing and receiving audio."""
        self.stop_playing()
        self.stop_listening()

    # @property
    # def sink(self):
    #     return self._reader.sink if self._reader else None

    # @sink.setter
    # def sink(self, value):
    #     if not isinstance(value, ConsumerAudio):
    #         raise TypeError('expected AudioSink not {0.__class__.__name__}.'.format(value))

    #     if self._reader is None:
    #         raise ValueError('Not receiving anything.')

    #     self._reader._set_sink(sink)
