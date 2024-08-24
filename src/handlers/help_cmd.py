from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

import src.keyboards.default.reply as kb
import src.states.user as user_states
from src.data.config import SUPPORT_IDS
from src.bot import bot

from ConfigFromJsonToDict import config_data

help_router = Router()

texts_help_cmd = config_data['texts']['help_cmd']

command = texts_help_cmd['command']

start_handler_button = eval(texts_help_cmd['start_handler_button'])

back_start_handler_button = config_data['texts']['keyboards']['reply']['back_kb']['buttons']

reply_buttons = config_data['texts']['keyboards']['reply']['help_kb']['buttons']

answer_messages = texts_help_cmd['answer_messages']

@help_router.message(Command(commands=command))
@help_router.message(F.text == start_handler_button)
@help_router.message(F.text == back_start_handler_button, StateFilter(user_states.UserFSM.write_message))
async def help_cmd(message: types.Message, state: FSMContext):
    await message.answer(answer_messages['main_help_text'], reply_markup=kb.help_kb)
    await state.set_state(user_states.UserFSM.help_menu)


@help_router.message(F.text == reply_buttons['call'], StateFilter(user_states.UserFSM.help_menu))
async def call(message: types.Message):
    await message.answer(answer_messages['call_text_answer'], reply_markup=kb.help_kb)


@help_router.message(F.text == reply_buttons['write'], StateFilter(user_states.UserFSM.help_menu))
async def write(message: types.Message, state: FSMContext):
    await message.answer(answer_messages['write_text_answer'], reply_markup=kb.back_kb)
    await state.set_state(user_states.UserFSM.write_message)

@help_router.message(StateFilter(user_states.UserFSM.write_message))
async def message_to_support(message: types.Message, state: FSMContext):
    await message.answer(answer_messages['message_to_support_arrived'], reply_markup=kb.help_kb)
    for SUPPORT_ID in SUPPORT_IDS:
        await bot.send_message(SUPPORT_ID, eval(answer_messages['to_support_message']))
    await state.set_state(user_states.UserFSM.help_menu)


