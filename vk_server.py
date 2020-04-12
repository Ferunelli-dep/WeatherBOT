import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import commands as cmd
from command_scripts import commands_scripts
from Database import DataBase


class vk_server:
    def __init__(self, token, bot_id, db):
        self.vk = vk_api.VkApi(token=token)
        self.longpoll = VkBotLongPoll(self.vk, bot_id)
        self.vk_api = self.vk.get_api()
        self.db = db

    def start(self):
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                msg = self.get_message(event).lower()
                if msg != '':
                    if event.from_user:
                        command = commands_scripts(self.vk_api, event)
                        user_id = self.get_user_id(event)
                        user_name = self.get_user_name(user_id)
                        if msg in cmd.commands and not self.db.get_user_state(user_id):
                            eval(cmd.commands[msg])
                        elif self.db.get_user_state(user_id) == 1:
                            command.input_city(user_id, msg)
                        elif self.db.get_user_state(user_id) == 2:
                            command.input_region(user_id, msg)
                        else:
                            self.send_message('К сожалению я не знаю такой команды :\'(\n'
                                              'Попробуй ввести другую.'
                                              'Если вдруг ты не знаешь команды, то я тебе подскажу\n'
                                              'Просто введи слово \"Помощь\"', event)

    def send_message(self, message, event):
        self.vk_api.messages.send(peer_id=event.obj.message['from_id'],
                                  user_id=self.get_user_id(event),
                                  random_id=get_random_id(),
                                  message=message)

    @staticmethod
    def get_user_id(event):
        return event.object['message']['from_id']

    def get_user_name(self, user_id):
        return self.vk_api.users.get(user_id=user_id)[0]['first_name']

    @staticmethod
    def get_message(event):
        return event.obj.message['text']