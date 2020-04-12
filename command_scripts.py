import data
from Database import DataBase
from vk_api.utils import get_random_id
from weather_script import weather
import random


class commands_scripts:
    def __init__(self, vk_session, event, keyboard):
        self.db = DataBase(data.database['host'], data.database['username'],
                           data.database['password'], data.database['database'],
                           data.database['port'])
        self.vk_api = vk_session
        self.event = event
        self.cursor, self.connection = self.db.connect()
        self.keyboard = keyboard

    def __send_message(self, message, event, user_id):
        self.vk_api.messages.send(peer_id=event.obj.message['from_id'],
                                  user_id=user_id,
                                  random_id=get_random_id(),
                                  message=message,
                                  keyboard=self.keyboard)

    def abort(self, user_id):
        self.db.set_user_state(user_id, 0)
        self.__send_message("Я тебя понял, уже отменяю!", self.event, user_id)

    def add_city(self, user_id):
        self.db.set_user_state(user_id, 1)
        self.__send_message("Пожалуйста, введи свой город.", self.event, user_id)

    def city_info(self, user_id):
        city_info = self.db.get_user_city(user_id)
        if city_info:
            self.__send_message("Город: {}\nРегион: {}".format(city_info[0], city_info[1]),
                                self.event, user_id)
        else:
            self.__send_message("Ты еще не ввёл свой город. Нажми на кнопку \"Добавить город\"", self.event, user_id)

    def help(self, user_id):
        self.__send_message("Хочешь добавить город? Жми на кнопку \"Добавить Город\"\n"
                            "Если ты это уже сделал, то кликни на кнопку \"Погода\"\n"
                            "Ну, а есди ты вдруг забыл какой город ты ввёл, "
                            "то спроси у меня, я с радостью тебе помогу, "
                            "Для этого просто намекни мне нажав \"Мой город\" и я тебе обязательно отвечу. \n"
                            "Если вдруг справка тебе не помогла, то смело @ferunelli(пиши сюда)",
                            self.event, user_id)

    def hello(self, user_id, user_name):
        self.__send_message("Привет, {}! \n"
                            "Я рад, что ты со мной.".format(user_name),
                            self.event, user_id)

    def input_city(self, user_id, message):
        if message == "отмена":
            self.abort(user_id)
        else:
            with self.cursor as cursor:
                cursor.execute("""UPDATE `user_info` 
                                  SET UserCity='{}' 
                                  WHERE UserID={}""".format(message.capitalize(), user_id))
                self.connection.commit()
                self.__send_message("Пожалуйста, введи свой регион "
                                    "(А чтобы мне было проще искать, регион должен быть в формате RU, UA, US и т.д.)",
                                    self.event, user_id)
            self.db.set_user_state(user_id, 2)

    def input_region(self, user_id, message):
        if message == "отмена":
            self.abort(user_id)
        else:
            with self.cursor as cursor:
                check_weather = weather(self.db.get_user_city(user_id)[0], data.API, region=message)
                if check_weather.check():
                    cursor.execute("""UPDATE `user_info` 
                                      SET UserRegion='{}' 
                                      WHERE UserID={}""".format(message.upper(), user_id))
                    self.connection.commit()
                    self.__send_message("Я запомнил, где ты живешь ;-) "
                                        "Я с радостью расскажу тебе про погоду в твоём городе, если ты напишешь"
                                        "\"Погода\"",
                                        self.event, user_id)
                    self.db.set_user_state(user_id, 0)
                else:
                    self.__send_message("К сожалению я не смог найти никаких городов с такими данными :-(\n"
                                        "Попробуй ввести другие.",
                                        self.event, user_id)
                    cursor.execute("""UPDATE `user_info` 
                                      SET UserCity=NULL, UserRegion=NULL
                                      WHERE UserID={}""".format(user_id))
                    self.connection.commit()
                    self.db.set_user_state(user_id, 0)

    def start(self, user_id, user_name):
        state = self.db.add_user_to_bd(user_id, user_name)
        if state:
            self.__send_message("Привет, {}, ты тут новенький!".format(user_name) +
                                "Я умею показывать погоду в твоём городе."
                                "Для начала введи команду \"Добавить Город\", чтобы я знал, какой город тебе интересен."
                                , self.event, user_id)
        else:
            self.__send_message("Если тебе нужна справка по командам, то введи \"Помощь\"\n"
                                "Я с радостью тебе всё расскажу :-)",
                                self.event, user_id)

    def weather(self, user_id):
        city_info = self.db.get_user_city(user_id)
        if city_info:
            current = weather(city_info[0], data.API, region=city_info[1])
            weather_now = current.get_weather_now()
            beginning = ["Что ж, готовься читать, я принес тебе много информации.\n Начнем с того, что",
                         "В общем,",
                         "Что ж,",
                         "Итак, ",
                         "Ну поехали, я набрал информацию и теперь готов тебе её доложить,"]
            text = random.choice(beginning) + \
                   " максимум температура поднимется до {} градусов, " \
                   "в среднем будет где-то {}. Скорость ветра может быть около {} км/ч, " \
                   "а влажность будет в районе {}%. " \
                   "В целом будет {}. ".format(weather_now['temp_max'],
                                               (weather_now['temp'] + weather_now['temp_min']) / 2,
                                               weather_now['wind_speed'], weather_now['humidity'],
                                               weather_now['weather'])

            end = ""
            # Погода - температура
            if abs(weather_now['temp_max'] - weather_now['temp_min']) > 10:
                end = "Скачок между температурами будет немаленький, поэтому будь предусмотрительным и возьми с собой " \
                      "вещей и на ту и на другую температуру. "
            elif weather_now['temp_min'] < -10:
                end += "Сегодня очень холодно, оденься как можно теплее. "
            elif -10 <= weather_now['temp'] < 0:
                end += "Сегодня холодновато. Ухх. Без куртки никак не выйдешь. "
            elif 0 <= weather_now['temp'] <= 10:
                end += "Эх, я бы не сказал, что очень жарко, надо надеть куртку. Если что, снимешь. "
            elif 10 < weather_now['temp'] < 20:
                end += "В целом, тепло, но я бы посоветовал тебе что-то с собой прихватить. "
            elif weather_now['temp'] > 20:
                end += "Достаточно жарко, я бы пошел в футболке. "

            # Влажность
            if 35 < weather_now['humidity'] < 60:
                end += "Думаю, стоит сегодня взять зонт или хотя бы плащ. "
            elif weather_now['humidity'] > 60:
                end += "Не забудь взять с собой зонт. "
            elif 15 < weather_now['humidity'] < 35:
                end += "Вот даже не знаю, советовать ли тебе брать зонт." \
                       " В целом, вероятность дождя не такая уж и большая. "
            # Ветер
            if weather_now['wind_speed'] > 20:
                end += "Также сегодня будет сильный ветер, будь очень аккуратен"

            self.__send_message(text + end, self.event, user_id)
        else:
            self.__send_message("К сожалению я ничего пока про тебя не знаю :-(\n"
                                "Введи команду \"Добавить город\" и расскажи немного о себе.", self.event, user_id)
