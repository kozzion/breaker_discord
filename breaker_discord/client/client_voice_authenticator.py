from pathlib import Path
import random
import json
import time
import sys
import hashlib

from breaker_core.datasource.jsonqueue import Jsonqueue
from breaker_core.datasource.bytessource import Bytessource
from breaker_discord.client.client import Client

class ClientVoiceAuthenticator(Client):

    def __init__(
        self,
        jsonqueue_request:Jsonqueue,
        bytessource_response:Bytessource) -> None:
        super(ClientVoiceAuthenticator, self).__init__(jsonqueue_request, bytessource_response)

    def encode(
        self,
        bytessource_sound:Bytessource,
        bytessource_encoding:Bytessource, 
        *,
        force_reprocess=True):
        print(bytessource_sound.path)
        print(bytessource_encoding.path)
        print(bytessource_sound.exists())
        print(bytessource_encoding.exists())

        dict_request = {}
        dict_request['type_request'] = 'encode' 
        dict_request['bytessource_voice_sound'] = bytessource_sound.to_dict()
        dict_request['bytessource_voice_encoding'] = bytessource_encoding.to_dict()
        return self.await_response(dict_request, force_reprocess)

    
    def authenticate(
        self,
        bytessource_sound:Bytessource,
        bytessource_encoding_dir:Bytessource,
        *,
        force_reprocess:bool=False):

        dict_request = {}
        dict_request['type_request'] = 'authenticate' 
        dict_request['bytessource_voice_sound'] = bytessource_sound.to_dict()
        dict_request['bytessource_voice_encoding_dir'] = bytessource_encoding_dir.to_dict()
        return self.await_response(dict_request, force_reprocess)
    
    