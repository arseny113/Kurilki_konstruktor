from aiogram import types, Router, F

from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from aiogram_dialog import DialogManager

import src.database.requests as rq
import src.keyboards.default.reply as kb
import src.keyboards.inline.yes_no_board as inkb
from src.handlers.registration import start_registration_name

router = Router()


# команда старт
@router.message(CommandStart())
@router.message(F.data == 'to_main')
@router.message(F.text == 'Главное меню')
async def start(message: types.Message, state: FSMContext, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    if await rq.check_user(message.from_user.id):
        await message.answer(f'Добро пожаловать в наш магазин, выберите необходимую опцию', reply_markup=kb.start)
    else:
        await message.answer(f'Здравствуйте! Вам есть 18 лет?"', reply_markup=inkb.yes_no_kb)

@router.callback_query(F.data == 'no')
async def cancellation(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f'К сожалению вы не можете пользоваться нашим магазином')
    await state.set_state(default_state)

@router.callback_query(F.data == 'yes')
async def start_registration(callback: types.CallbackQuery, state: FSMContext):
    await start_registration_name(callback.message, state)
