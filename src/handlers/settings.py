from aiogram import types, Router, F
from aiogram.filters import StateFilter, or_f, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from aiogram_dialog import DialogManager

import src.database.requests as rq
import src.keyboards.default.reply as kb
import src.states.user as user_states

from ConfigFromJsonToDict import config_data

texts_settings = config_data['texts']['settings']

command = texts_settings['command']

start_handler_button = eval(texts_settings['start_handler_button'])

back_start_handler_button = config_data['texts']['keyboards']['reply']['back_kb']['buttons']

reply_buttons = config_data['texts']['keyboards']['reply']['settings_kb']['buttons']

answer_messages = texts_settings['answer_messages']

settings_router = Router()


@settings_router.message(Command(commands=texts_settings['command']))
@settings_router.message(F.text == start_handler_button)
@settings_router.message(F.text == back_start_handler_button, or_f(StateFilter(user_states.UserFSM.rewrite_name),
                                                 StateFilter(user_states.UserFSM.rewrite_phone),
                                                 )
                         )
async def settings_setup(message: types.Message, state: FSMContext, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    await message.answer(answer_messages['settings_setup'], reply_markup=kb.settings_kb)
    await state.set_state(user_states.UserFSM.settings_menu)


@settings_router.message(F.text == reply_buttons['setting_name'])
async def setting_name(message: types.Message, state: FSMContext):
    name = await rq.get_name(tg_id=message.from_user.id)
    await message.answer(answer_messages['setting_name'], reply_markup=kb.back_kb)
    await state.set_state(user_states.UserFSM.rewrite_name)


@settings_router.message(F.text == reply_buttons['setting_phone'])
async def setting_phone(message: types.Message, state: FSMContext):
    phone = await rq.get_number(tg_id=message.from_user.id)
    await message.answer(answer_messages['setting_phone'], reply_markup=kb.back_kb)
    await state.set_state(user_states.UserFSM.rewrite_phone)


@settings_router.message(StateFilter(user_states.UserFSM.rewrite_name))
async def rename(message: types.Message, state: FSMContext):
    await rq.update_name_phone(message.from_user.id, name=message.text)
    await message.answer(answer_messages['rename'], reply_markup=kb.settings_kb)
    await state.set_state(default_state)


@settings_router.message(StateFilter(user_states.UserFSM.rewrite_phone))
async def rephone(message: types.Message, state: FSMContext):
    await rq.update_name_phone(message.from_user.id, phone=message.text)
    await message.answer(answer_messages['rephone'], reply_markup=kb.settings_kb)
    await state.set_state(default_state)

