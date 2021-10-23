import os
import json

from breaker_core.datasource.jsonqueue import Jsonqueue
from breaker_core.datasource.bytessource import Bytessource

from breaker_discord.client.client_voice_synthesizer import ClientVoiceSynthesizer

path_file_config_breaker = os.environ['PATH_FILE_CONFIG_BREAKER']
with open(path_file_config_breaker, 'r') as file:
    dict_config = json.load(file)


jsonqueue_request = Jsonqueue.from_dict(dict_config['queue_request_voice_synthesizer'])
bytessource_response = Bytessource.from_dict(dict_config['bytessource_response_voice_synthesizer'])
bytessource_output = Bytessource.from_dict(dict_config['bytessource_output_voice_synthesizer'])
bytessource_voice = Bytessource.from_dict(dict_config['bytessource_voice_sound']).join(['102797880246419456', '1634755367'])


client = ClientVoiceSynthesizer(jsonqueue_request, bytessource_response, bytessource_output)



response, bytessource_output = client.synthesize('eng', bytessource_voice, 'jaap is a super great programmer', force_reprocess=True)
print(response)
print(bytessource_output.exists())