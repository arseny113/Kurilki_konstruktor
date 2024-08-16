from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Row,
    ScrollingGroup,
    Select
)
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.media import StaticMedia
from aiogram.types import ContentType
import operator

from ConfigFromJsonToDict import config_data

from .states import states, Catalog_levels
from .getters import get_level, get_item
from .callbacks import selected_level, to_item, to_cart, to_main, increment, decrement, quant


level_windows = []

texts_catalog_dialog_windows = config_data['texts']['catalog']['dialog']['windows']
levels_choice_count = int(config_data['texts']['catalog']['dialog']['levels_choice_count'])

for window in range(levels_choice_count):
    if window == 0:
        level_windows.append(Window(
            Const(texts_catalog_dialog_windows[f'level_{window}_message']),
            ScrollingGroup(
                Select(
                    id=f"Level_{window}",
                    items=f"lvl{window}",
                    item_id_getter=operator.itemgetter(1),
                    text=Format("{item[0]}"),
                    on_click=selected_level,
                ),
                id=f"lvl{window}_group",
                height=10,
                width=1,
                hide_on_single_page=True
            ),
        Button(Const(texts_catalog_dialog_windows['to_main_button']), id="to_main", on_click=to_main),
        state=states[window],
        getter=get_level,
        ))
    elif window == levels_choice_count - 1:
        level_windows.append(Window(
            Const(texts_catalog_dialog_windows[f'level_{window}_message']),
            ScrollingGroup(
                Select(
                    id=f"Level_{window}",
                    items=f"lvl{window}",
                    item_id_getter=operator.itemgetter(1),
                    text=Format("{item[0]}"),
                    on_click=to_item,
                ),
                id=f"lvl{window}_group",
                height=10,
                width=1,
                hide_on_single_page=True
            ),
            Back(Const(texts_catalog_dialog_windows['back_button'])),
            Button(Const(texts_catalog_dialog_windows['to_main_button']), id="to_main", on_click=to_main),
            state=states[window],
            getter=get_level,
        ))

    else:
        level_windows.append(Window(
            Const(texts_catalog_dialog_windows[f'level_{window}_message']),
            ScrollingGroup(
                Select(
                    id=f"Level_{window}",
                    items=f"lvl{window}",
                    item_id_getter=operator.itemgetter(1),
                    text=Format("{item[0]}"),
                    on_click=selected_level,
                ),
                id=f"lvl{window}_group",
                height=10,
                width=1,
                hide_on_single_page=True
            ),
        Back(Const(texts_catalog_dialog_windows['back_button'])),
        Button(Const(texts_catalog_dialog_windows['to_main_button']), id="to_main", on_click=to_main),
        state=states[window],
        getter=get_level,
        ))


product_card_window = Window(
        StaticMedia(
        path=Format('{image}'),
        type=ContentType.PHOTO,
    ),
        Format(text=texts_catalog_dialog_windows['product_cart_message']),
        Row(Button(Const(texts_catalog_dialog_windows['decrement_button']), id="decrement", on_click=decrement),
                    Button(Format(texts_catalog_dialog_windows['quant_button']), id="quant", on_click=quant),
                    Button(Const(texts_catalog_dialog_windows['increase_button']), id="increment", on_click=increment)),
        Row(Button(Const(texts_catalog_dialog_windows['to_main_button']), id="to_main", on_click=to_main),
                    Button(Const(texts_catalog_dialog_windows['to_cart_button']), id='to_cart', on_click=to_cart),
                    Back(Const(texts_catalog_dialog_windows['back_button'])),),
        state=Catalog_levels.item,
        getter=get_item,
    )

Catalog_lvl1 = Dialog(
             *level_windows,
    product_card_window,
)


