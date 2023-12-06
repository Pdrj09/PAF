"""
    PAF Core
    Timer and task list module
"""
from collections import deque
import asyncio
import os
import time
import wave
import whisper
import pyaudio

class Stt():
    """
        Class to transcribe a audio to a text (Speech To Text):
            model: str -> "tiny", "base", "small", "medium", "large" (base as default)
            language: str -> get of the setting
            time: int -> time of the records (s)
    """

    def __init__(self, model: str = "base", record_time: int = 10) -> None:

        self.model = whisper.load_model(model)
        self.record_time = record_time
        self.queue = deque()
        self.audio = pyaudio.PyAudio()
        self.FORMAT=pyaudio.paInt16
        self.CHANNELS=2
        self.RATE=44100
        self.CHUNK=1024

    def record(self):
        """
            Record audios of time seconds 
        """
        stream = self.audio.open(format=self.FORMAT,channels=self.CHANNELS,
                                rate=self.RATE, input=True,
                                frames_per_buffer=self.CHUNK)
        frames = []

        for i in range(0, int(self.RATE/self.CHUNK*self.record_time)):
            data = stream.read(self.CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        loc = f'./tmp_{time.time()}.wav' # modificar la dirección del fichero
        audio = wave.open(loc, 'wb')
        audio.setnchannels(self.CHANNELS)
        audio.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        audio.setframerate(self.RATE)
        audio.writeframes(b''.join(frames))
        audio.close()
        self.queue.append(loc)
        return self.queue

    def decoder(self):
        """
            Transcribe an audio for a text
        """
        try:
            file = self.queue.popleft()
            text = self.model.transcribe(file)
            os.remove(file)
            return text

        except IndexError:
            print('ups')
