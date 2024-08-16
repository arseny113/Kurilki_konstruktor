from aiogram import types, Router, F

from aiogram.filters import Command

from aiogram_dialog import DialogManager, StartMode

catalog_router = Router()

from src.dialogs.Catalog.states import Catalog_levels, states

from ConfigFromJsonToDict import config_data

texts_catalog_handler = config_data['texts']['catalog']['handler']

@catalog_router.message(Command(commands=texts_catalog_handler['command']))
@catalog_router.message(F.text == texts_catalog_handler['reply_button'])
async def catalog_lvl1(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(Catalog_levels.level_0, mode=StartMode.RESET_STACK)

@catalog_router.callback_query(F.data == texts_catalog_handler['callback_data'])
async def catalog_lvl1_answ(callback: types.CallbackQuery, dialog_manager: DialogManager):
    await callback.message.delete()
    await dialog_manager.start(Catalog_levels.level_0, mode=StartMode.RESET_STACK)
