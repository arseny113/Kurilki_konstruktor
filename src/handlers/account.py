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

start_handler_button = eval(config_data['start_handler_button'])

command = texts_account['command']

reply_buttons = config_data['texts']['account_kb']['buttons']

answer_messages = texts_account['answer_messages']



@account_router.message(Command(commands=command))
@account_router.message(F.text == start_handler_button)
async def to_personal_account(message: types.Message, state: FSMContext, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    await message.answer(answer_messages['to_personal_account_message'], reply_markup=kb.account_kb)


@account_router.message(F.text == reply_buttons['history'])
async def history(message: types.Message):
    order_message = answer_messages['history_start_message']
    orders = await rq.get_orders(message.from_user.id)
    for order in orders:
        prod_id = order.prod_id
        product = await rq.get_product(prod_id)
        order_message += eval(answer_messages['history_pattern_message'])
    if orders:
        await message.answer(order_message, reply_markup=kb.account_kb)
    else:
        await message.answer(texts_account["history_none_message"], reply_markup=kb.account_kb)
