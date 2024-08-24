from src.handlers.common import router
from src.handlers.help_cmd import help_router
from src.handlers.settings import settings_router
from src.handlers.registration import registration_router
from src.handlers.catalog import catalog_router
from src.handlers.cart import cart_router
from src.handlers.order import order_router
from src.dialogs.Catalog.catalog_dialogs import Catalog
from src.dialogs.Cart.cart_dialogs import Cart
from src.handlers.account import account_router
from src.handlers.faq import faq_router


routers_table = {
    "router": router,
    "registration_router": registration_router,
    "account_router": account_router,
    "catalog_router": catalog_router,
    "settings_router": settings_router,
    "faq_router": faq_router,
    "cart_router": cart_router,
    "order_router": order_router,
    "help_router": help_router,
    "Catalog": Catalog,
    "Cart": Cart
}

def names_2_routers(routers_list: list):
    return [routers_table[router_name] for router_name in routers_list]