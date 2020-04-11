import data
from WeatherScript import Weather
from Database import DB
import pymysql

current = Weather("Москва", region="RU", API=data.API)

db = DB(data.database['host'], data.database['username'],
        data.database['password'], data.database['database'],
        data.database['port'])

if db.test():
    print(db.test())
else:
    print("NOpe")

