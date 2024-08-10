from aiogram.fsm.state import State, StatesGroup

class Catalog_levels(StatesGroup):
    level_0 = State()
    level_1 = State()
    level_2 = State()
    level_3 = State()
    item = State()
    select_item = State()
