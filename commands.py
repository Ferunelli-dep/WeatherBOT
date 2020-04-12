from command_scripts import commands_scripts as command

commands = {
    'начать': 'command.start(user_id, user_name)',
    'start': 'command.start(user_id, user_name)',
    'погода': 'command.weather(user_id)',
    'добавить город': 'command.add_city(user_id)',
    'привет': 'command.hello(user_id, user_name)',
    'мой город': 'command.city_info(user_id)',
    'помощь': 'command.help(user_id)'
}
