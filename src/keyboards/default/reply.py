from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Сделать заказ')],
    [KeyboardButton(text='Личный кабинет'), KeyboardButton(text='Вопросы и ответы')],
], resize_keyboard=True, input_field_placeholder='Выберете необходимую опцию')

back_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Назад')],
], resize_keyboard=True, one_time_keyboard=True)

settings_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Имя'), KeyboardButton(text='Номер')],
                                            [KeyboardButton(text='Главное меню')]],
                                  resize_keyboard=True, one_time_keyboard=True)

send_contact_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Отправить свой контакт', request_contact=True)]
], resize_keyboard=True, one_time_keyboard=True)

