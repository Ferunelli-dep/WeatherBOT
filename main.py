import data
from WeatherScript import Weather

current = Weather("Куйбышево", region="RU", API=data.API)

print(current.getWeatherNow())
