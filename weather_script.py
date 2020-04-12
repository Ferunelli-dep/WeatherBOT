import requests


class weather:
    def __init__(self, place, API, region=""):
        self.place = place
        self.region = region
        self.API = API
        self.URL = "http://api.openweathermap.org/data/2.5/weather"
        self.params = {'q': self.place + ',' + self.region, 'units': 'metric', 'lang': 'ru', 'APPID': self.API}
        self.proxies = {
            'http': 'http://80.187.140.26:8080',
            'https': 'http://31.14.131.70:8080'
        }

    def check(self):
        res = requests.get(self.URL, self.params, proxies=self.proxies)
        data = res.json()
        if 'message' in data:
            return False
        else:
            return data

    def get_weather_now(self):
        proxy_state = True
        while proxy_state:
            try:
                city_info = self.check()
                if not city_info:
                    return 'Not found'
                proxy_state = False
            except requests.exceptions.ProxyError:
                continue
        city_data = {
            'temp': city_info['main']['temp'],
            'temp_min': city_info['main']['temp_min'],
            'temp_max': city_info['main']['temp_max'],
            'wind_speed': city_info['wind']['speed'],
            'humidity': city_info['main']['humidity'],
            'weather': city_info['weather'][0]['description'],
            'city': city_info['name'],
            'region': city_info['sys']['country']
        }

        return city_data
