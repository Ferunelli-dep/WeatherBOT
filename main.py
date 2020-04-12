import data
from Database import DataBase
from vk_server import vk_server
import vk_api
import pymysql

db = DataBase(data.database['host'], data.database['username'],
              data.database['password'], data.database['database'],
              data.database['port'])

while True:
    try:
        vk = vk_server(data.vk_token, data.bot_id, db)
        vk.start()
    except vk_api.exceptions.ApiError:
        print("Неверно указаны данные для работы Бота")
        break
    except pymysql.err.OperationalError:
        print("Неверно указаны данные для работы с БД")
        break
    except:
        continue

