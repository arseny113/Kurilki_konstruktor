from aiogram import Router, types, F

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from src.bot import bot
import src.database.requests as rq

from src.database.models import Order, async_session

from src.data.config import MANAGER_ID

from ConfigFromJsonToDict import config_data


order_router = Router()

texts_order = config_data['texts']['order']

start_handler_data = texts_order['start_handler_data']

answer_messages = texts_order['answer_messages']


@order_router.callback_query(F.data == 'continue')
async def sending_order(callback: types.CallbackQuery, widget: Button, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    await callback.message.delete()
    products = [(await rq.get_product(order.prod_id), order.amount) for order in
                                      await rq.orm_get_user_carts(callback.from_user.id)]
    product_strings = [eval(texts_order['product_string_pattern']) for product in products]
    username = callback.from_user.username
    name = await rq.get_name(callback.from_user.id)
    phone_number = await rq.get_number(callback.from_user.id)
    manager_message = ''
    for string in answer_messages['answer_to_manager']:
        manager_message += eval(string) + '\n'
    await bot.send_message(MANAGER_ID,
                           manager_message +
                           "\n".join([string for string in product_strings]),)
    await callback.message.answer(answer_messages['answer_to_buyer'])
    await rq.orm_update_status(callback.from_user.id, 'shop', 'in_progress')


