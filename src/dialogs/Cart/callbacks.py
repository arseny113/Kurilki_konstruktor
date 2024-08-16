from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, Select
from .states import Cart_levels
from ..Catalog.states import Catalog_levels

import src.keyboards.default.reply as kb

import src.database.requests as rq

from ConfigFromJsonToDict import config_data

texts_cart_dialog_callbacks = config_data['texts']['cart']['dialog']['callbacks']

async def to_main(callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,):
    await dialog_manager.done()
    await callback_query.message.answer(texts_cart_dialog_callbacks['to_main_message'], reply_markup=kb.start_kb)

async def selected_product(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.dialog_data["product_id"] = int(item_id)
    await dialog_manager.switch_to(Cart_levels.product_card)

async def delete(callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,):
    await rq.orm_delete_from_cart(callback_query.from_user.id, dialog_manager.current_context().dialog_data.get('product_id'))
    if await rq.orm_get_user_carts(callback_query.from_user.id) == []:
        await dialog_manager.done()
        await callback_query.message.delete()
        await callback_query.message.answer(texts_cart_dialog_callbacks['empty'])
    else:
        await dialog_manager.switch_to(Cart_levels.select_products)

async def reduce(callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,):
    prod_del = await rq.orm_reduce_product_in_cart(callback_query.from_user.id, dialog_manager.current_context().dialog_data.get('product_id'))
    if not prod_del:
        print(rq.orm_get_user_carts(callback_query.from_user.id))
        if await rq.orm_get_user_carts(callback_query.from_user.id) == []:
            await dialog_manager.done()
            await callback_query.message.delete()
            await callback_query.message.answer(texts_cart_dialog_callbacks['empty'])
        else:
            await dialog_manager.switch_to(Cart_levels.select_products)

async def increase(callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,):
    await rq.orm_add_to_cart(callback_query.from_user.id, dialog_manager.current_context().dialog_data.get('product_id'), 1)

async def to_catalog(callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,):
    await dialog_manager.done()
    await callback_query.answer(texts_cart_dialog_callbacks['to_catalog_answer'])
    await dialog_manager.start(Catalog_levels.level_0, mode=StartMode.RESET_STACK)


