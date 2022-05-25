import sounddevice as sd 
from scipy.io.wavfile import write 
import wavio as wv 


freq = 44100
duration = 5

recording = sd.rec(int(duration * freq),  
                    samplerate=freq, channels=2)



sd.wait() 

write("paf_core/rec/recording.wav", freq, recording) 

wv.write("recording1.wav", recording, freq, sampwidth=2)