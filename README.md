# Умный сервис прогноза погоды (Уровень 3 Со звездочкой)
## Проектирование сервиса
  В качестве языка был выбран язык программирования **Python**. Было решено реализовать ВК бота и для связи с интерфейсом **VK** была использована библиотека **vk_api**. На запрос пользователя посмотреть погоду, бот будет выдавать сообщение с различными (случайно выбранными) вступлениями (```"Что ж, готовься читать, я принес тебе много информации.Начнем с того, что", "В общем,","Что ж,","Итак, ", "Ну поехали, я набрал информацию и теперь готов тебе её доложить,"```) далее идет основная часть ответа, в которой содержится основная информация о погоде (```максимум температура поднимется до {} градусов, в среднем будет где-то {}. Скорость ветра может быть около {} км/ч, а влажность будет в районе {}%. Будет {}```) и далее следует заключительная часть, в которой бот даёт советы по тому, что лучше надеть и суммирает как-то информацию о погоде. Советы бот выбирает исходя из того, какая температура, скорость ветра и влажность в это городе. (Пример совета ```В целом, тепло, но я бы посоветовал тебе что-то с собой прихватить. Вот даже не знаю, советовать ли тебе брать зонт. В целом, вероятность дождя не такая уж и большая.```)
Пример ответа бота: ```Итак, максимум температура поднимется до 8 градусов, в среднем будет где-то 7.2. Скорость ветра может быть около 3 км/ч, а влажность будет в районе 33%. Будет пасмурно. Эх, я бы не сказал, что очень жарко, надо надеть куртку. Если что, снимешь. Вот даже не знаю, советовать ли тебе брать зонт. В целом, вероятность дождя не такая уж и большая.```
## Демонстрация работы

## Описание процесса работы бота
  Бот высылает ответ пользователю исходя из его команды. Если команда неверная, бот будет писать, что команда не найдена. Если команда распознана.
  + Бот проверяет, есть ли пользователь в базе данных, если его нет, то Бот отправляет запрос в базу данных и вносит пользователя с текущим **ID**.
  + Бот ищет команду в списке и выполняет функцию, которая там указана.
  + Команда **Помощь** отправляет пользователю информацию по командам, которые есть в боте.
  + Команда **Добавить Город**.
    + Формируется запрос в базу данных и пользователю присваивается статус 1, что означает, что пользователь нажал на кнопку **Добавить город**. Бот ожидает следующее сообщение
    + Когда сообщение приходит, бот отправляет запрос в базу данных и присваивает полю **UserCity** то, что ввёл пользователю и полю **UserState** значение 2, что означает, что пользователь ввёл название города. Бот ожидает следующее сообщение.
    + Когда приходит название региона, бот отправляет запрос в базу данных и получает введённый ранее город из поля **UserCity**. Далее, бот обращается к API прогноза погоды и проверяет, есть ли по указанным данным какая либо информация о погоде. Если бот находит эту информацию, то бот обновляет в базе данных поле **UserRegion** с тем сообщением, которое отправил пользователь полю **UserState** присваивает значение 0, что означает, что бот ожидает стандартных команд. При **UserState** 1 и **UserState** 2, бот может так же ожидать команду "отмена" при которой он отменит все изменения введённые пользоваталем и присвоит полю UserState значение 0, продолжая ожидать следующие команды.
  + Команда **Мой город**
    + Бот отправляет запрос в базу данных для получения полей **UserCity** и **UserRegion**, если в этих полях лежат значения ***NULL***, это значит, что у пользователя нет информации о его городе. В этом случае бот информирует пользователя о том, что город не указан. В ином случае, бот отправляет пользователю информацию о его городе и регионе.
  + Команда **Погода**
    + Бот отправляет запрос в базу данных для получения полей **UserCity** и **UserRegion**, если в этих полях лежат значения ***NULL***, это значит, что у пользователя нет информации о его городе. В этом случае бот информирует пользователя о том, что город не указан.
    + Если город и регигон указаны, бот обращается к API погоды и получает информацию о погоде в текущем городе. 
    + Формируется ответ и отправляется пользователю
## Запуск приложения
Для того, чтобы запустить данного бота для начала вам нужно иметь python3 и установить библиотеки ```vk_api``` и ```pymysql``` для него.
Сделать это можно командами:
```
pip install vk_api 
pip install pymysql
```
Далее вам необходимо создать файл ```data.py``` со следующим содержанием.
``` python
API = "openweathermap_API" # Получить можно по ссылке https://openweathermap.org/api
database = {
    'host': "database_hostname",
    'username': "database_username",
    'password': "database_password",
    'database': "database_name",
    'port': database_port
}
vk_token = "Токен бота"
bot_id = ID бота
```
Далее переходим в папку с проектом и запускаем файл ```main.py``` командой
```
python3 main.py
```
Работоспособность программы проверена на OC Ubuntu.
### Настройка бота для получения API и корректной работы
 - Для начала вам нужно создать сообщество вконтакте
 - Далее перейдите в сообщество и нажимаем кнопку "Управление"
 - После этого откройте вкладку **Работа с API** и во вкладке **Ключи доступа** генерируем ключ. Его надо будет вставить в файл ```data.py``` в переменную **vk_token**.
 - Во вкладке **Long POLL API** вам нужно включить **Long POLL API** и выбрать последнюю версию этого API
 - Во вкладке **Типы событий** ставим все галочки.
 - Далее нам нужно узнать ID сообщества. Для этого выйдем из настроек и скопируем ссылку на сообщество.
 - https://regvk.com/id/ вставляем ссылку сюда и видим наш ID, его надо вставить в файл ```data.py``` в переменную ```bot_id```
