'''
    PAF - Personal Assistant, Free
    weather.py - Weather module of PAF_core
'''
import requests
import json


# Class to get the actual weather of a city
class tem_actual():

    def __init__(self):
        # Get the settigns of the application
        open('paf_core/settings.json', 'r')
        settings = json.load(open('paf_core/settings.json', 'r'))
        # Load the weather settings
        settings = settings['weather']
        self.settings = settings

    # get the data of the weather
    def dat(self, city):
        url = 'http://api.openweathermap.org/data/2.5/weather?q=%1s&appid=%2s&lang=%3s&units=%4s' % (city, self.settings['apiKey'], 
                                                                                                        self.settings['lenguage'], 
                                                                                                        self.settings['units'])
        out = requests.get(url)
        data = out.json()
        self.data = data
        del out
        del data
        del url
    
    def resf(self, data):
        if self.data == None:
            self.data = data

    # get the temperature of the data
    def temp(self):
        temp = self.data['main']['temp']
        wind = self.data['wind']['speed']
        humidity = self.data['main']['humidity']
        sens_temp = self.data['main']['feels_like']
        description = self.data['weather'][0]['description']
        icon = self.data['weather'][0]['icon']

        dic_tem = {'temp':temp, 'sens':sens_temp, 'humi':humidity, 'vient':wind, 'des':description, 'icon':icon}
        
        del temp, wind, description, humidity, sens_temp

        return dic_tem

    # get the localitation of the data
    def location(self):

        loc = {"lat":str(self.data['coord']['lat']), 'lon':str(self.data['coord']['lon'])}

        return loc

# Class for get all the forecast of the city
class one_call():

    def __init__(self):
        # Get the settigns of the application
        open('paf_core/settings.json', 'r')
        settings = json.load(open('paf_core/settings.json', 'r'))
        # Load the weather settings
        settings = settings['weather']
        self.settings = settings

    # dat of the forecast
    def dat(self, lat, lon):
        """lat = int(loc['lat'])
        lon = int(loc['lon'])"""

        """url = 'https://api.openweathermap.org/data/2.5/onecall?lat=%1s&lon=%2s&appid=%3s&exclude=current&units=%4s'%(lat, lon,
                                                                                                                            self.settings['apiKey'], 
                                                                                                                            self.settings['units'])"""
        url = 'https://api.openweathermap.org/data/2.5/onecall?lat=%1s&lon=%2s&appid=%3s&units=%4s'%(lat, lon,
                                                                                                                            self.settings['apiKey'], 
                                                                                                                            self.settings['units'])
        
        out = requests.get(url)
        data = out.json()
        self.data = data

        return data

        #del lat, lon, url, out, data

    # get the rain information of the city
    def min(self):
        w = self.data['hourly'][0]['weather'][0]['main']
        if w == 'Thunderstorm' or w == 'Rain' or w == 'Snow':
            prep = {}
            for n in range(0,61):

                prep[n] = self.data['minutely'][n]['precipitation']
        else:
            prep = None

        return prep
    
    # get the information of the city hour by hour
    def hour(self):
        hour = {}
        dic_1 = self.data['hourly']
        for n in range(0,48):
            dic = {'temp': dic_1[n]['temp'], 'humidity':dic_1[n]['humidity'], 'feels_like':dic_1[n]['feels_like'], 'icon':dic_1[n]['weather'][0]['icon']}
            hour[n] = dic
        
        del dic_1, dic
        return hour
    
    # get the uvi data of the city hour by hour
    def uvi(self):
        uvi = {}
        for n in range(0,48):
            uvi[n] = self.data['hourly'][n]['uvi']
            
        return uvi

    # get the forecast by day
    def day(self):
        day = {}
        dic_1 = self.data['daily']
        for n in range(0,8):
            dic = {'temp_max': dic_1[n]['temp']['max'],'temp_min': dic_1[n]['temp']['min'], 'humidity':dic_1[n]['humidity'], 'feels_like':dic_1[n]['feels_like']['day'], 'icon':dic_1[n]['weather'][0]['icon'], 'description':dic_1[n]['weather'][0]['description']}
            day[n] = dic
        
        del dic_1, dic
        return day
    
    # get the alert of the weather
    def ale(self):
        try:
            al = self.data['alerts']
            return al
        except:
            al = None
            return al

