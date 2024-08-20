from aiogram import types, Router, F

from aiogram.filters import Command

from aiogram_dialog import DialogManager, StartMode
from src.dialogs.Cart.states import Cart_levels

from ConfigFromJsonToDict import config_data
import src.database.requests as rq
import src.keyboards.default.reply as kb

cart_router = Router()

texts_cart_handler = config_data['texts']['cart']['handler']

command = texts_cart_handler['command']

start_handler_button = eval(texts_cart_handler['start_handler_button'])

answer_messages = texts_cart_handler['answer_messages']

callback_data = texts_cart_handler['callback_data']

# корзина
@cart_router.message(Command(commands=command))
@cart_router.message(F.text == start_handler_button)
async def get_carts(message: types.Message, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    if await rq.orm_get_user_carts(message.from_user.id) == []:
        await message.answer(answer_messages['empty'], reply_markup=kb.start_kb)
    else:
        await dialog_manager.start(Cart_levels.select_products, data={'user_id': message.from_user.id}, mode=StartMode.RESET_STACK)

@cart_router.callback_query(F.data == callback_data['get_carts_call_1'])
@cart_router.callback_query(F.data == callback_data['get_carts_call_2'])
async def get_carts_call(callback: types.CallbackQuery, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    if await rq.orm_get_user_carts(callback.from_user.id) == []:
        await callback.answer(texts_cart_handler['empty'], reply_markup=kb.start_kb)
    else:
        await dialog_manager.start(Cart_levels.select_products, data={'user_id': callback.from_user.id}, mode=StartMode.RESET_STACK)
