from aiogram import types, Router, F

from aiogram.filters import CommandStart, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from aiogram_dialog import DialogManager

import src.database.requests as rq
import src.keyboards.default.reply as kb
import src.keyboards.inline.yes_no_board as inkb
from src.handlers.registration import start_registration_name
import src.states.user as user_states

router = Router()


@router.message(CommandStart(), ~or_f(StateFilter(user_states.UserFSM.write_name),
                                      StateFilter(user_states.UserFSM.write_phone),
                                      StateFilter(user_states.UserFSM.write_email),
                                      StateFilter(user_states.UserFSM.rewrite_name),
                                      StateFilter(user_states.UserFSM.rewrite_phone),
                                      StateFilter(user_states.UserFSM.rewrite_email),
                                      ))
@router.message(F.data == 'to_main')
@router.message(F.text == 'Главное меню')
async def start(message: types.Message, state: FSMContext, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    if await rq.check_user(message.from_user.id):
        await message.answer(f'Добро пожаловать в наш магазин, выберите необходимую опцию', reply_markup=kb.start_kb)
    else:
        await message.answer(f'Здравствуйте! Вам есть 18 лет?', reply_markup=inkb.yes_no_kb)


@router.callback_query(F.data == 'no')
async def cancellation(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(f'К сожалению, Вы не можете пользоваться нашим магазином')
    await state.set_state(default_state)


@router.callback_query(F.data == 'yes')
async def start_registration(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await rq.set_user(callback.from_user.id)
    await start_registration_name(callback.message, state)
