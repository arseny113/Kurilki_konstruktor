from aiogram import types, Router, F

from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from aiogram_dialog import DialogManager

import src.database.requests as rq
import src.keyboards.default.reply as kb

account_router = Router()


@account_router.message(F.text == 'Личный кабинет')
async def to_personal_account(message: types.Message, state: FSMContext, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    await message.answer("Вы перешли в личный кабинет\nВыберете необходимую опцию", reply_markup=kb.account_kb)
