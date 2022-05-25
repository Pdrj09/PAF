#import the tts and stt modules, import additional modules for the agent
import logging
from traceback import print_tb

from pandas import array
from torch import float16
from models.stt_model import model as stt
import models.tts_model as tts
import numpy as np
import wave

print('cargando el asistente')
logger = logging
logger.warning('iniciando el programa')

def stt_models():
    audio_buffer = wave.open("paf_core/rec/recording1.wav", "r")
    audio_buffer = wave.rewind(audio_buffer)
    logger.critical(audio_buffer)
    #audio = np.int16(audio_buffer)
    logger.warning('cargando el asistente')
    sttm = stt('stt/model.tflite')
    #sttm.enableExternalScorer('stt/kenlm_es.scorer')
    logger.warning('procesando audio')
    p = sttm.stt()
    print(p)


stt_models()