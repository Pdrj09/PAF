"""
    PAF Core
    Weather module
"""
import logging
import requests

try:
    import paf_core.settings as settings
except ModuleNotFoundError:
    import settings

KEY = settings.settings['apis']['weather']['apiKey']
LAN = settings.LAN
UNITS = settings.UNITS

# create the log
logger = logging.getLogger('log_config')


class TemActual:
    """Class to get the current weather of a city"""

    def __init__(self):

        self.data = None

    # get the data of the weather
    def dat(self, city):
        """Funtion of TemActual to get the weather data"""

        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={KEY}\
&lang={LAN}&units={UNITS}'

        try:

            #try to connect to the server and get the weather data
            out = requests.get(url, timeout=100)
            data = out.json()
            logger.info('request status -> OK')
            status = 200

        except requests.exceptions.ConnectionError:
            logger.critical('FATAL ERROR -> fail requests')
            status = 500

        except requests.exceptions.Timeout:
            logger.critical('TIME OUT ERROR -> fail request')

        self.data = data
        del out, data, url
        return status

    def resf(self, data: dict):
        """Restarts the data of a dictionary if the data is equal to None"""

        if self.data is None:
            self.data = data

    def temp(self):
        """Get the temperature data form the weather data"""

        temp = self.data['main']['temp']
        wind = self.data['wind']['speed']
        humidity = self.data['main']['humidity']
        sens_temp = self.data['main']['feels_like']
        description = self.data['weather'][0]['description']
        icon = self.data['weather'][0]['icon']

        dic_tem = {
            'temp': temp,
            'sens': sens_temp,
            'humi': humidity,
            'vient': wind,
            'des': description,
            'icon': icon,
        }

        del temp, wind, description, humidity, sens_temp

        return dic_tem

    def location(self):
        """Get the localization of the request"""

        loc = {
            'lat': str(self.data['coord']['lat']),
            'lon': str(self.data['coord']['lon']),
        }

        return loc


class OneCall:
    """Class to get all the weather information of the city"""

    def __init__(self):
        self.data = None
        self.status = None

    def dat(self, lat, lon):
        """Function on the cas"""

        url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}\
                &appid={KEY}&units={UNITS}'

        try:

            # Saving data as a JSON
            out = requests.get(url, timeout=100)
            data = out.json()

            # Updating the Data and the Status of the server (to change)
            logger.info('request status -> OK')
            self.data = data
            self.status = 200

            return data

        except requests.exceptions.ConnectionError:

            logger.critical('FATAL ERROR -> fail requests')
            return self.status

        except requests.exceptions.Timeout:
            logger.critical('TIMEOUT ERROR -> fail request')

    def min(self):
        """Get the rain forecast of the city"""

        weather_data = self.data['hourly'][0]['weather'][0]['main']
        if (
            weather_data == 'Thunderstorm'
            or weather_data == 'Rain'
            or weather_data == 'Snow'
        ):

            prep = {}
            for minute_data in range(0, 61):
                prep[minute_data] = self.data['minutely'][minute_data]['precipitation']
        else:
            prep = None

        return prep

    # Gets information of the city hour by hour
    def hour(self):
        """Get the information hour by hour of the request"""

        hour = {}
        dic_1 = self.data['hourly']
        for hour_data in range(0, 48):
            dic = {
                'temp': dic_1[hour_data]['temp'],
                'humidity': dic_1[hour_data]['humidity'],
                'feels_like': dic_1[hour_data]['feels_like'],
                'icon': dic_1[hour_data]['weather'][0]['icon'],
            }

            hour[hour_data] = dic

        del dic_1, dic
        return hour

    # get the uvi data of the city hour by hour
    def uvi(self):
        """Get the UVI information of every our in the next 48 hours"""

        uvi = {}
        for hour_uvi in range(0, 48):
            uvi[hour_uvi] = self.data['hourly'][hour_uvi]['uvi']

        return uvi

    def day(self):
        """Get the daily weather" for the next 8 days"""

        day = {}
        dic_1 = self.data['daily']

        for day_forecast in range(0, 8):

            dic = {
                'temp_max': dic_1[day_forecast]['temp']['max'],
                'temp_min': dic_1[day_forecast]['temp']['min'],
                'humidity': dic_1[day_forecast]['humidity'],
                'feels_like': dic_1[day_forecast]['feels_like']['day'],
                'icon': dic_1[day_forecast]['weather'][0]['icon'],
                'description': dic_1[day_forecast]['weather'][day_forecast][
                    'description'
                ],
            }

            day[day_forecast] = dic

        del dic_1, dic
        return day

    # get the alert of the weather
    def ale(self):
        """Get the meteorological alerts"""

        try:
            met_alerts = self.data['alerts']
            return met_alerts

        except KeyError:
            met_alerts = None
            return met_alerts
