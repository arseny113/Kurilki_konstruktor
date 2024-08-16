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

from .states import Cart_levels
from .getters import get_products, get_item
from .callbacks import to_main, selected_product, delete, increase, reduce, to_catalog
from src.handlers.order_registration import sending_order
from ConfigFromJsonToDict import config_data

texts_cart_dialog_windows = config_data['texts']['cart']['dialog']['windows']

products_window = Window(
        Format(texts_cart_dialog_windows['cart_message']),
        ScrollingGroup(
            Select(
                id="select",
                items="products",
                item_id_getter=operator.itemgetter(0),
                text=Format("{item[1]}"),
                on_click=selected_product,
            ),
            id="products_group",
            height=10,
            width=1,
            hide_on_single_page=True
        ),
        Row(Button(Const(texts_cart_dialog_windows['to_main_button']), id="to_main", on_click=to_main),
            Button(Const(texts_cart_dialog_windows['to_catalog_button']), id="to_catalog", on_click=to_catalog)),
        Button(Const(texts_cart_dialog_windows['make_order_button']), id="to_payment", on_click=sending_order),
        state=Cart_levels.select_products,
        getter=get_products,
    )

product_window = Window(
        StaticMedia(
        path=Format('{image}'),
        type=ContentType.PHOTO,
    ),
        Format(texts_cart_dialog_windows['product_card_message']),
        Row(Button(Const(texts_cart_dialog_windows['delete_button']), id="delete", on_click=delete),
            Button(Const(texts_cart_dialog_windows['increase_button']), id="increase", on_click=increase),
            Button(Const(texts_cart_dialog_windows['reduce_button']), id="reduce", on_click=reduce)),
        Row(Button(Const(texts_cart_dialog_windows['to_main_button']), id="to_main", on_click=to_main),
            Button(Const(texts_cart_dialog_windows['to_catalog_button']), id="to_catalog", on_click=to_catalog),
            Back(Const(texts_cart_dialog_windows['back_button']))),
        Button(Const(texts_cart_dialog_windows['make_order_button']), id="to_payment", on_click=sending_order),
        state=Cart_levels.product_card,
        getter=get_item,
    )


Cart = Dialog(
    products_window,
             product_window,
)

