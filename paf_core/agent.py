#import the tts and stt modules
import models.stt_model as stts
import models.tts_model as tts
import numpy as np
from pydub import AudioSegment

song = AudioSegment.from_wav("paf_core/tts_output.wav")

def stt_models():
    audio_buffer = "paf_core/tts_output.wav"
    audio_buffer_0 = np.int16(audio_buffer)
    print(audio_buffer_0)
    sttm = stts.model('STT/model.tflite')
    sttm.enableExternalScorer('STT/kenlm_es.scorer')
    p = sttm.stt(song)
    print(p)

stt_models()





'''import pyaudio

class AudioRecorder():

    N = 4096 #chunk
    format = pyaudio.paInt16
    channels = 1
    rate = 44100
    T = 1/rate
    
    def __init__(self):
        self.p = pyaudio.PyAudio()

  
    def callbackFunc(self, in_data, frame_count, time_info, status_flags):
        print("Callback...")
        self.sock.sendall(in_data)
        return (in_data, pyaudio.paContinue)
    
    
    def openStream(self):
        self.stream = self.p.open(format=self.format,
                channels= self.channels,
                rate= self.rate,
                input=True,
                frames_per_buffer= self.N,
                stream_callback = self.callbackFunc)

p = AudioRecorder()
p.openStream()'''