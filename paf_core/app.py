import weather
import time

v = weather.one_call()
l = weather.tem_actual()
l.dat('Madrid')
loc = l.location()

while True:
    v.dat(loc)
    print(v)
    time.sleep(10000)