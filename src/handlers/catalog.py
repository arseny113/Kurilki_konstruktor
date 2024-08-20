from aiogram import types, Router, F

from aiogram.filters import Command

from aiogram_dialog import DialogManager, StartMode

catalog_router = Router()

from src.dialogs.Catalog.states import states

from ConfigFromJsonToDict import config_data

texts_catalog_handler = config_data['texts']['catalog']['handler']

command = texts_catalog_handler['command']

reply_buttons = texts_catalog_handler['reply_buttons']

callback_data = texts_catalog_handler['callback_data']

@catalog_router.message(Command(commands=command))
@catalog_router.message(F.text == reply_buttons['catalog_lvl1'])
async def catalog_lvl1(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(states[0], mode=StartMode.RESET_STACK)

@catalog_router.callback_query(F.data == callback_data['catalog_lvl1_answ'])
async def catalog_lvl1_answ(callback: types.CallbackQuery, dialog_manager: DialogManager):
    await callback.message.delete()
    await dialog_manager.start(states[0], mode=StartMode.RESET_STACK)
