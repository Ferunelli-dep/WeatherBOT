import data
from WeatherScript import Weather
from Database import DataBase
from vk_server import vk_server
import pymysql


# current = Weather("Москва", region="RU", API=data.API)

# db = DataBase(data.database['host'], data.database['username'],
#               data.database['password'], data.database['database'],
#               data.database['port'])

vk = vk_server(data.vk_token, data.bot_id)
vk.start()



