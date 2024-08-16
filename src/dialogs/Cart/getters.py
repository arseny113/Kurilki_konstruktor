from src.database.models import async_session, Order, Catalog
from sqlalchemy import select
from src.utils.funcs import get_image_size, get_image_ratio
from src.database.requests import get_order_price
from aiogram_dialog import DialogManager
from ConfigFromJsonToDict import config_data


texts_cart_dialog_getters = config_data['texts']['cart']['dialog']['getters']

#получение товаров в корзине
async def get_products(dialog_manager: DialogManager, **middleware_data):
     async with async_session() as session:
        db_main = await session.scalars(select(Order.prod_id).where(Order.tg_id == dialog_manager.current_context().start_data.get('user_id'), Order.status == 'shop'))
        products = [(item, await session.scalar(select(Catalog).where(Catalog.id == item))) for item in db_main]
        data = {
            'products': [(item, eval(texts_cart_dialog_getters['product_info'])) for item, product in products],
        }
        return data


async def get_item(dialog_manager: DialogManager, **middleware_data):
    async with async_session() as session:
        db_main = await session.scalar(
            select(Catalog).where(Catalog.id == dialog_manager.current_context().dialog_data.get('product_id')))
        db_quant = await session.scalar(select(Order.amount).where(Order.prod_id == dialog_manager.current_context().dialog_data.get('product_id')))
        keys = texts_cart_dialog_getters['product_card_getter']
        data = {'image': db_main.image,
                'quant': db_quant}
        for key in keys:
            try:
                data[key] = eval(f"db_main.{key}")
            except:
                pass
        return data

