import data
from WeatherScript import Weather
from Database import DB
from vk_server import vk_server
import pymysql


current = Weather("Москва", region="RU", API=data.API)

db = DB(data.database['host'], data.database['username'],
        data.database['password'], data.database['database'],
        data.database['port'])


vk = vk_server(data.vk_token, data.bot_id)
vk.start()


if db.test():
    print(db.test())
else:
    print("NOpe")


