from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


yes_no_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Пройти Регистрацию', callback_data='yes'),],
])
