from aiogram import Router, types, F

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from src.bot import bot
import src.database.requests as rq

from src.data.config import MANAGER_ID


order_registration_router = Router()


#@order_registration_router.callback_query(F.data == 'continue')
async def sending_order(callback: types.CallbackQuery, widget: Button, dialog_manager: DialogManager):
    data = dialog_manager.current_context().dialog_data
    product = await rq.get_product(int(data.get('item_id')))
    quant = data.get("quant")
    try:
        await dialog_manager.done()
    except:
        pass

    await rq.write_to_order(callback.from_user.id, int(data.get('item_id')), quant)
    await callback.message.delete()
    await bot.send_message(MANAGER_ID,
                           f"Новый заказ от пользователя @{callback.from_user.username}\nна имя: {await rq.get_name(callback.from_user.id)}\nНомер телефона: {await rq.get_number(callback.from_user.id)}\n"
                           f"{product[0]} {product[1]} {product[2]} в количестве: {quant} шт.")
    await callback.message.answer("Ваш заказ обработан и передан менеджеру, ожидайте дальнейшей связи")

