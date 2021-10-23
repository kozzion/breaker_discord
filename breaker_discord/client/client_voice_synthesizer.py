from pathlib import Path
import random
import json
import time
import sys
import hashlib

from breaker_core.tools_general import ToolsGeneral
from breaker_core.datasource.jsonqueue import Jsonqueue
from breaker_core.datasource.bytessource import Bytessource

from breaker_discord.client.client import Client

class ClientVoiceSynthesizer(Client):


    def __init__(
        self,
        jsonqueue_request:Jsonqueue,
        bytessource_response:Bytessource,
        bytessource_output:Bytessource) -> None:
        super(ClientVoiceSynthesizer, self).__init__(jsonqueue_request, bytessource_response)
        self.bytessource_output = bytessource_output
        
    def synthesize(
        self,
        language_code_639_3:str,
        bytessource_voice:Bytessource,
        text:str,
        *,
        force_reprocess=False):

        dict_request = {}
        dict_request['type_request'] = 'synthesize' 
        dict_request['language_code_639_3'] = language_code_639_3
        dict_request['bytessource_voice'] = bytessource_voice.to_dict()
        dict_request['text'] = text
        hash_request = ToolsGeneral.sha256_dict_json(dict_request)
        bytessource_output = self.bytessource_output.join([hash_request])
        dict_request['bytessource_output'] = bytessource_output.to_dict()
        return self.await_response(dict_request, force_reprocess), bytessource_output
