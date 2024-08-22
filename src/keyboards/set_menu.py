from aiogram import Bot
from aiogram.types import BotCommand

from ConfigFromJsonToDict import config_data

handlers = config_data['texts']

bot_commands = config_data['commands']

async def set_main_menu(bot: Bot):
    main_menu_commands = []

    for handler in handlers:
        command, description = handlers[handler].get('command'), handlers[handler].get('command_description')
        if not command:
            try:
                command, description = handlers[handler]['handler'].get('command'), handlers[handler]['handler'].get('command_description')
            except:
                pass
        if command and command in bot_commands:
            main_menu_commands.append(BotCommand(command=f'/{command}', description=description))
    await bot.set_my_commands(main_menu_commands)
