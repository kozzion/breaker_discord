from pathlib import Path
import random
import json
import time
import sys
import hashlib

from breaker_core.datasource.jsonqueue import Jsonqueue
from breaker_core.datasource.bytearraysource import Bytearraysource

class ClientBreakerAudioTts:

    def __init__(
        self,
        jsonqueue_request:Jsonqueue) -> None:
        
        self.jsonqueue_request = jsonqueue_request

    def synthesize(
        self,
        language_code_639_3:str,
        bytearraysource_voice:Bytearraysource,
        text:str,
        bytearraysource_output:Bytearraysource):

        dict_request = {}
        dict_request['language_code_639_3'] = language_code_639_3
        dict_request['bytearraysource_voice'] = bytearraysource_voice.to_dict()
        dict_request['text'] = text
        dict_request['bytearraysource_output'] = bytearraysource_output.to_dict()
 
        if bytearraysource_output.exists():
            print('response found')
            sys.stdout.flush()
            return
        else:
            print('writing request')
            sys.stdout.flush()
            self.jsonqueue_request.enqueue(dict_request)

            while(True):
                if bytearraysource_output.exists():
                    time.sleep(0.001)
                    return
                else:
                    time.sleep(0.1)

