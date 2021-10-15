

import numpy as np
import opus
from opus import encoder, decoder
class ToolsOpus:

    @staticmethod
    def opus_to_array_int16_pcm(list_bytearray_opus):

        sample_rate = 48000
        channel_count = 1
        frame_size = 960
        
        # 16 * 2.5 = 40 (very rare)
        # 16 * 5 = 80 (rare)
        # 16 * 10 = 160
        # 16 * 20 = 320
        # 16 * 40 = 640
        # 16 * 60 = 960

        decoder = opus.decoder.Decoder(sample_rate, channel_count)
        
        
        
        bytearray_pcm = bytearray()
        for bytearray_opus in list_bytearray_opus:
            pcm_decoded = decoder.decode(bytearray_opus, frame_size)
            bytearray_pcm.extend(pcm_decoded[:1920])
        return np.frombuffer(bytearray_pcm, np.int16), sample_rate
