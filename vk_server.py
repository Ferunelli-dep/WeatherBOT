import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import commands as cmd


class vk_server:
    def __init__(self, token, bot_id):
        self.vk = vk_api.VkApi(token=token)
        self.longpoll = VkBotLongPoll(self.vk, bot_id)
        self.vk_api = self.vk.get_api()

    def start(self):
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                msg = self.get_message(event)
                if msg != '':
                    if event.from_user:
                        if msg.lower() in cmd.commands:
                            self.send_message('Команда распознана', event)
                        else:
                            self.send_message('К сожалению мне не удалось распознать вашу команду :\'(\n'
                                              'Попробуйте ввести другую.', event)

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