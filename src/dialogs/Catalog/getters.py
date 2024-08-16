from src.database.models import async_session, Catalog, lvl_names
# lvl2_base, lvl3_base, lvl4_base, lvl5_base
from sqlalchemy import select, distinct, desc
from src.utils.funcs import get_image_size, get_image_ratio
from .states import states
from aiogram_dialog import DialogManager

from ConfigFromJsonToDict import config_data


texts_catalog_dialog_getters = config_data['texts']['catalog']['dialog']['getters']

#получение значений для 3 уровня
async def get_level(dialog_manager: DialogManager, **middleware_data):
     async with async_session() as session:
        dialog_data = dialog_manager.current_context().dialog_data
        level = states.index(dialog_manager.current_context().state)
        expression = f'select(Catalog.{lvl_names[level]}, Catalog.id)'
        for now_level in range(level):
            if now_level == 0:
                expression = expression + ".where("
            now_level_name = await session.scalar(eval(f"select(Catalog.{lvl_names[now_level]}).where(Catalog.id == {dialog_data[f'level{now_level}']})"))
            expression = expression + f'Catalog.{lvl_names[now_level]} == "{now_level_name}", '
            if level == now_level + 1:
                expression = expression + ")"
        db_main_query = eval(expression + f'.distinct(Catalog.{lvl_names[level]})')
        db_main_result = await session.execute(db_main_query)
        data = {f'lvl{level}': [(item[0], item[1]) for item in db_main_result.all()]}
        return data


#получение карточки товара
async def get_item(dialog_manager: DialogManager, **middleware_data):
     async with async_session() as session:
        db_main = await session.scalar(select(Catalog).where(Catalog.id == dialog_manager.current_context().dialog_data.get('item_id')))
        keys = texts_catalog_dialog_getters['product_card_getter']
        quant = dialog_manager.current_context().dialog_data.get('quant')
        data = {'image': db_main.image,
                'quant': quant}
        for key in keys:
            data[key] = eval(f"db_main.{key}")
        return data
