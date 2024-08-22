from aiogram import types, Router, F

from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from aiogram_dialog import DialogManager

import src.database.requests as rq
import src.keyboards.default.reply as kb

from ConfigFromJsonToDict import config_data

faq_router = Router()

texts_faq = config_data['texts']['faq']

command = texts_faq['command']

start_handler_button = eval(texts_faq['start_handler_button'])

reply_buttons_faq = config_data['texts']['keyboards']['reply']['faq_kb']['buttons']

reply_buttons_questions = config_data['texts']['keyboards']['reply']['questions_kb']['buttons']

start_back_handler_button = reply_buttons_questions['back']

answer_messages = texts_faq['answer_messages']

@faq_router.message(F.text == start_handler_button)
@faq_router.message(F.text == start_back_handler_button)
@faq_router.message(Command(commands=command))
async def faq(message: types.Message, state: FSMContext, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    await message.answer(answer_messages['to_faq'], reply_markup=kb.faq_kb)


@faq_router.message(F.text == reply_buttons_faq['general_questions'])
async def general_questions(message: types.Message):
    await message.answer(answer_messages['to_general_questions'], reply_markup=kb.questions_kb)


@faq_router.message(F.text == reply_buttons_faq['contacts'])
async def contacts(message: types.Message):
    await message.answer(answer_messages['to_contacts'], reply_markup=kb.faq_kb)

@faq_router.message(F.text == reply_buttons_questions['how_to_order'])
async def how_to_order(message: types.Message):
    await message.answer(answer_messages['how_to_order'], reply_markup=kb.questions_kb)

@faq_router.message(F.text == reply_buttons_questions['brands'])
async def brands(message: types.Message):
    await message.answer(answer_messages['brands'], reply_markup=kb.questions_kb)