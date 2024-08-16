from aiogram.fsm.state import State, StatesGroup
from ConfigFromJsonToDict import config_data

levels_choice_count = int(config_data['texts']['catalog']['dialog']['levels_choice_count'])

states = []
class Catalog_levels(StatesGroup):
    for lvl in range(levels_choice_count):
        locals()[f"level_{lvl}"] = State(f"level_{lvl}")
        states.append(locals()[f"level_{lvl}"])
    item = State()
    select_item = State()
