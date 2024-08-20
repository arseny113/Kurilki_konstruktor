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

from ConfigFromJsonToDict import config_data

router = Router()

texts_common = config_data['texts']['common']

start_handler_button = texts_common['start_handler_button']

start_handler_data = texts_common['start_handler_data']

answer_messages = texts_common['answer_messages']

callback_data = texts_common['callback_data']

@router.message(CommandStart(), ~or_f(StateFilter(user_states.UserFSM.write_name),
                                      StateFilter(user_states.UserFSM.write_phone),
                                      StateFilter(user_states.UserFSM.rewrite_name),
                                      StateFilter(user_states.UserFSM.rewrite_phone),
                                      ))
@router.message(F.data == start_handler_data)
@router.message(F.text == start_handler_button)
async def start(message: types.Message, state: FSMContext, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    if await rq.check_user(message.from_user.id):
        await message.answer(answer_messages['start_text_registered_answer'], reply_markup=kb.start_kb)
    else:
        await message.answer(answer_messages['start_text_unregistered_answer'], reply_markup=inkb.yes_no_kb)


@router.callback_query(F.data == callback_data['registration_apply_data'])
async def start_registration(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await rq.set_user(callback.from_user.id)
    await start_registration_name(callback.message, state)
