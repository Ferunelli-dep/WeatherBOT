import data
from Database import DataBase
from vk_server import vk_server

db = DataBase(data.database['host'], data.database['username'],
              data.database['password'], data.database['database'],
              data.database['port'])


vk = vk_server(data.vk_token, data.bot_id, db)
vk.start()
