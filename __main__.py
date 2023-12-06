""""
    PAF -> Personal Assistant, Free
"""
from paf_core import stt, weather

def main():
    audio = stt.Stt()
    audio.record()
    text = audio.decoder()

    if text['text'] == ' Dame la temperatura atmosférica.':
        temp=weather.TemActual()
        temp.dat('Madrid')
        print(temp.temp())
    else:
        print(text['text'])


if __name__ == '__main__':
    try:
        while True:
            main()
    except:
        pass
