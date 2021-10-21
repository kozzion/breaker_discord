from pathlib import Path
import random
import json
import time
import sys
import hashlib

from breaker_core.datasource.jsonqueue import Jsonqueue
from breaker_core.datasource.bytessource import Bytessource

from breaker_discord.client.client import Client

class ClientBreakerAudioTts(Client):

    def __init__(
        self,
        jsonqueue_request:Jsonqueue) -> None:
        super.__init__(jsonqueue_request)

    def synthesize(
        self,
        language_code_639_3:str,
        bytessource_voice:Bytessource,
        text:str,
        bytessource_output:Bytessource):

        dict_request = {}
        dict_request['language_code_639_3'] = language_code_639_3
        dict_request['bytessource_voice'] = bytessource_voice.to_dict()
        dict_request['text'] = text
        dict_request['bytessource_output'] = bytessource_output.to_dict()
        self.await_response(dict_request, bytessource_output)
