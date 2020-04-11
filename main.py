import data
from WeatherScript import Weather

currentCity = Weather("Москва", region="RU", API=data.API)

currentWeather = currentCity.getWeatherNow()

print(currentWeather)