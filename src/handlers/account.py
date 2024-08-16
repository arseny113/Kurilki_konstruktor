from aiogram import types, Router, F

from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from aiogram_dialog import DialogManager

import src.database.requests as rq
import src.keyboards.default.reply as kb

from ConfigFromJsonToDict import config_data

account_router = Router()

texts_account = config_data['texts']['account']
string_pattern_orders = texts_account["orders_pattern_message"]


@account_router.message(Command(commands=texts_account['command']))
@account_router.message(F.text == texts_account['reply_buttons'][0])
async def to_personal_account(message: types.Message, state: FSMContext, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    await message.answer(texts_account['to_p_a_message'], reply_markup=kb.account_kb)


@account_router.message(F.text == texts_account['reply_buttons'][1])
async def history(message: types.Message):
    order_message = texts_account['orders_start_message']
    orders = await rq.get_orders(message.from_user.id)
    for order in orders:
        prod_id = order.prod_id
        product = await rq.get_product(prod_id)
        order_message += eval(string_pattern_orders)
    if orders:
        await message.answer(order_message, reply_markup=kb.account_kb)
    else:
        await message.answer(texts_account["history_none_message"], reply_markup=kb.account_kb)
