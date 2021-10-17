import sys

from breaker_core.datasource.bytearraysource import Bytearraysource
from breaker_discord.extension.processor.processor_opus import ProcessorOpus

class ProcessorOpusTrackSpeaker(ProcessorOpus):

    #def __init__(self, voice_client, bytearraysource_save:BytearraysourceGenerator) -> None:
        
    def __init__(self, voice_client, bytearraysource_conversation:Bytearraysource) -> None:
        super().__init__()
        self.voice_client = voice_client
        self.bytearraysource_conversation = bytearraysource_conversation
        self.dict_temp_storage = {}
        

    def update_user_dict(self, id_source, id_user):
        pass 

    def process(self, conversation_id:str, source_id:str, timestamp:int, sequence:int, bytearray_opus:bytearray):
        print('process!' + conversation_id)
        sys.stdout.flush()
        if not source_id in self.voice_client._ssrc_to_id:
            print('missing use user_id')
        else:
            user_id = self.voice_client._ssrc_to_id[source_id]
            print('saving')
            bytearraysource_save = self.bytearraysource_conversation.generate([conversation_id, user_id, timestamp])
            bytearraysource_save.save(bytearray_opus)

    def is_complete(self) -> bool:
        return False

    def create_overview(self, id_conversation):
        pass
