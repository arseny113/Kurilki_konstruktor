from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, Select
from .states import Catalog_levels
from ..Cart.states import Cart_levels
from ...database.requests import orm_add_to_cart
from ConfigFromJsonToDict import config_data
import src.keyboards.default.reply as kb
from .states import states

texts_catalog_dialog_callbacks = config_data['texts']['catalog']['dialog']['callbacks']


async def selected_level(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    level = states.index(dialog_manager.current_context().state)
    if not dialog_manager.dialog_data.get("user_id"):
        dialog_manager.dialog_data["user_id"] = callback_query.from_user.id
    await dialog_manager.switch_to(states[level + 1])
    dialog_manager.dialog_data[f'level{level}'] = int(item_id)


#запись id товара и переход к карточке
async def to_item(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.dialog_data["item_id"] = int(item_id)
    dialog_manager.dialog_data["quant"] = 1
    await dialog_manager.switch_to(Catalog_levels.item)


#добавление в корзину
async def to_cart(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await orm_add_to_cart(tg_id=callback_query.from_user.id, prod_id=dialog_manager.current_context().dialog_data.get('item_id'), quant=dialog_manager.dialog_data["quant"])
    await callback_query.answer(texts_catalog_dialog_callbacks["go_to_cart_answer"])
    await dialog_manager.switch_to(Catalog_levels.item)

async def to_main(callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,):
    await dialog_manager.done()
    await callback_query.message.answer(texts_catalog_dialog_callbacks["to_main_message"], reply_markup=kb.start_kb)

async def go_to_cart(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await callback_query.answer(texts_catalog_dialog_callbacks["go_to_cart_answer"])
    await dialog_manager.done()

    await dialog_manager.start(Cart_levels.select_products, data={'user_id': callback_query.from_user.id}, mode=StartMode.RESET_STACK)

async def increment(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    dialog_manager.dialog_data["quant"] += 1

async def decrement(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    if dialog_manager.dialog_data["quant"] > 1:
        dialog_manager.dialog_data["quant"] -= 1
    else:
        await callback_query.answer(texts_catalog_dialog_callbacks["cancel_decrement_answer"])
        dialog_manager.dialog_data["quant"] = 1

async def quant(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await callback_query.answer(f'{texts_catalog_dialog_callbacks['quant_button_answer']} {dialog_manager.dialog_data["quant"]}')
