from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from ConfigFromJsonToDict import config_data

keyboards = config_data['texts']['keyboards']['reply']

for keyboard_name in keyboards:
    keyboard = keyboards[f'{keyboard_name}']
    format_kb = [int(i) for i in keyboard['format']]
    buttons = []
    button_parameters = {}
    for button, value in keyboard['buttons'].items():
        if '_parameters' in button:
            button_parameters[f'{button.replace("_parameters", "")}'] = keyboard['buttons'][f'{button}']
            break
        else:
            buttons.append({'button': button, 'value': value})
    keyboard_parameters = keyboard.get('parameters')
    rows = []
    button_count = 0
    for row in format_kb:
        i_row = []
        for column in range(row):
            button_create_string = 'KeyboardButton(text='
            button_create_string += f'"{buttons[button_count]["value"]}"'
            i_button_parameters = button_parameters.get(f'{buttons[button_count]["button"]}')
            button_count += 1
            if i_button_parameters:
                for parameter, value in i_button_parameters.items():
                    if value == 'True' or value == 'False':
                        button_create_string += f', {parameter}={eval(value)}'
                    else:
                        button_create_string += f', {parameter}="{value}"'
            button_create_string += ')'
            i_row.append(eval(button_create_string))
        rows.append(i_row)
    keyboard_create_string = f'ReplyKeyboardMarkup(keyboard={rows}'
    if keyboard_parameters:
        for parameter, value in keyboard_parameters.items():
            if value == 'True' or value == 'False':
                keyboard_create_string += f', {parameter}={eval(value)}'
            else:
                keyboard_create_string += f', {parameter}="{value}"'
    keyboard_create_string += ')'
    locals()[keyboard_name] = eval(keyboard_create_string)



locals()['asdflsdfj'] =  ''

"""start_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Каталог'), KeyboardButton(text='Корзина')],
    [KeyboardButton(text='Личный кабинет'), KeyboardButton(text='Вопросы и ответы')],
], resize_keyboard=True, input_field_placeholder='Выберете необходимую опцию')

account_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Настройки')],
    [KeyboardButton(text='История заказов')],
    [KeyboardButton(text='Главное меню')],
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

faq_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Общие вопросы')],
                                       [KeyboardButton(text='Наши контакты')],
                                       [KeyboardButton(text='Главное меню')],
                                       ], resize_keyboard=True, one_time_keyboard=True)

questions_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Как сделать заказ?')],
                                             [KeyboardButton(text='Какие бренды поставляет наша компания?')],
                                             [KeyboardButton(text='Главное меню')]
                                             ], resize_keyboard=True, one_time_keyboard=True)

help_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Позвонить'), KeyboardButton(text='Написать')],
    [KeyboardButton(text='Главное меню')],
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Выберете необходимую опцию')"""