from src.database.models import async_session, Catalog
# lvl2_base, lvl3_base, lvl4_base, lvl5_base
from sqlalchemy import select, distinct, desc
from src.utils.funcs import get_image_size, get_image_ratio
from .states import Catalog_levels
from aiogram_dialog import DialogManager

from .states import Catalog_levels


order = ['SeaBear', 'Air Stick', 'EPE']
lvls_names = ['brand', 'puffs', 'flavor']
previous_choices = []

states = [Catalog_levels.level_0, Catalog_levels.level_1, Catalog_levels.level_2, Catalog_levels.level_3]

#получение значений для 3 уровня
async def get_level(dialog_manager: DialogManager, **middleware_data):
     async with async_session() as session:
        dialog_data = dialog_manager.current_context().dialog_data
        level = states.index(dialog_manager.current_context().state)
        expression = f'select(Catalog.{lvls_names[level]}, Catalog.id)'
        for now_level in range(level):
            if now_level == 0:
                expression = expression + ".where("
            now_level_name = await session.scalar(eval(f"select(Catalog.{lvls_names[now_level]}).where(Catalog.id == {dialog_data[f'level{now_level}']})"))
            expression = expression + f'Catalog.{lvls_names[now_level]} == "{now_level_name}", '
            if level == now_level + 1:
                expression = expression + ")"
        db_main_query = eval(expression + f'.distinct(Catalog.{lvls_names[level]})')
        db_main_result = await session.execute(db_main_query)
        data = {f'lvl{level}': [(item[0], item[1]) for item in db_main_result.all()],
                }
        return data


#получение значений для 4 уровня
async def get_level_4(dialog_manager: DialogManager, **middleware_data):
     async with async_session() as session:
        lvl3_name = await session.scalar(select(Catalog.brand).where(Catalog.id == int(dialog_manager.current_context().dialog_data.get('level_3'))))
        lvl = middleware_data.get('state')
        db_main = set(await session.scalars(select(Catalog.puffs).where(Catalog.brand == lvl3_name)))
        db_main_items = set(await session.scalars(select(Catalog).where(Catalog.brand == lvl3_name)))
        data = {'lvl4': [(puffs, await session.scalar(select(Catalog.id).where(Catalog.puffs == puffs))) for puffs in db_main],
                }
        return data

#получение значений для 5 уровня
async def get_level_5(dialog_manager: DialogManager, **middleware_data):
     async with async_session() as session:
        lvl3_name = await session.scalar(select(Catalog.brand).where(Catalog.id == int(dialog_manager.current_context().dialog_data.get('level_3'))))
        lvl4_name = await session.scalar(select(Catalog.puffs).where(Catalog.id == int(dialog_manager.current_context().dialog_data.get('level_4'))))
        db_main = set(await session.scalars(select(Catalog.flavor).where(Catalog.brand == lvl3_name, Catalog.puffs == lvl4_name)))
        data = {'lvl5': [(flavor, await session.scalar(select(Catalog.id).where(Catalog.flavor == flavor))) for flavor in db_main]}
        return data

#получение значений товаров
async def get_selected_items(dialog_manager: DialogManager, **middleware_data):
     async with async_session() as session:
        level = dialog_manager.current_context().dialog_data.get('select_items')
        if level == 'level_5':
            lvl2_name = await session.scalar(select(lvl2_base.level_2).where(lvl2_base.id == int(dialog_manager.current_context().dialog_data.get('level_2'))))
            lvl3_name = await session.scalar(select(lvl3_base.level_3).where(lvl3_base.id == int(dialog_manager.current_context().dialog_data.get('level_3'))))
            lvl4_name = await session.scalar(select(lvl4_base.level_4).where(lvl4_base.id == int(dialog_manager.current_context().dialog_data.get('level_4'))))
            db_main_items = set(await session.scalars(select(Catalog).where(Catalog.level_5 == '', Catalog.level_4 == lvl4_name, Catalog.level_3 == lvl3_name, Catalog.level_2 == lvl2_name)))
            data = {'item': [(f'{item.name.split()[-1]} ({item.price} Руб.)', item.id) for item in db_main_items]}
            return data
        else:
            lvl2_name = await session.scalar(select(lvl2_base.level_2).where(lvl2_base.id == int(dialog_manager.current_context().dialog_data.get('level_2'))))
            lvl3_name = await session.scalar(select(lvl3_base.level_3).where(lvl3_base.id == int(dialog_manager.current_context().dialog_data.get('level_3'))))
            lvl4_name = await session.scalar(select(lvl4_base.level_4).where(lvl4_base.id == int(dialog_manager.current_context().dialog_data.get('level_4'))))
            lvl5_name = await session.scalar(select(lvl5_base.level_5).where(lvl5_base.id == int(dialog_manager.current_context().dialog_data.get('level_5'))))
            db_main_items = set(await session.scalars(select(Catalog).where(Catalog.level_5 == lvl5_name, Catalog.level_4 == lvl4_name, Catalog.level_3 == lvl3_name, Catalog.level_2 == lvl2_name)))
            data = {'item': [(f'{item.name.split()[-1]} ({item.price} Руб.)', item.id) for item in db_main_items]}
            return data


#получение карточки товара
async def get_item(dialog_manager: DialogManager, **middleware_data):
     async with async_session() as session:
        db_main = await session.scalar(select(Catalog).where(Catalog.id == int(dialog_manager.current_context().dialog_data.get('item_id'))))

        data = {'brand': db_main.brand,
                'image': db_main.image,
                'flavor': db_main.flavor,
                'puffs': db_main.puffs,
                'quant': dialog_manager.current_context().dialog_data.get('quant'),
                'volume': db_main.volume,
                'nicotine': db_main.nicotine,
                'heat_element': db_main.heat_element,
                'battery': db_main.battery,
                'connector': db_main.connector,
                'compound': db_main.compound
                }

        return data
