from aiogram import types, Router, F

from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from aiogram_dialog import DialogManager

import src.database.requests as rq
import src.keyboards.default.reply as kb

faq_router = Router()


@faq_router.message(F.text == 'Вопросы и ответы')
async def to_faq(message: types.Message, state: FSMContext, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    await message.answer("Вы перешли в раздел с вопросами и ответами\nВыберете необходимую опцию", reply_markup=kb.faq_kb)


@faq_router.message(F.text == 'Общие вопросы')
async def to_general_questions(message: types.Message):
    await message.answer("Выберете интересующий вас вопрос", reply_markup=kb.questions_kb)


@faq_router.message(F.text == 'Наши контакты')
async def to_general_questions(message: types.Message):
    await message.answer("Номер телефона для связи: \nМенеджер: ", reply_markup=kb.faq_kb)
