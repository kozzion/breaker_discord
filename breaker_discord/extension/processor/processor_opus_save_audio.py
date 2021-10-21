import sys

from breaker_core.datasource.bytessource_generator import BytessourceGenerator
from breaker_discord.extension.processor.processor_opus import ProcessorOpus

class ProcessorOpusSaveAudio(ProcessorOpus):

    def __init__(self, voice_client, bytessource_save:BytessourceGenerator) -> None:
        self.voice_client = voice_client
        self.bytessource_save = bytessource_save
        self.dict_temp_storage = {}
        

    def update_user_dict(self, id_source, id_user):
        pass 

    def process(self, id_conversation:str, id_source:str, timestamp:int, sequence:int, bytearray_opus:bytearray):
        print('process!')
        sys.stdout.flush()
        # if id_source in self.voice_client.
        # id_user = 
        # self.bytessource_save.generate([id_conversation])

    def is_complete(self) -> bool:
        return False

    def create_overview(self, id_conversation):
        pass
