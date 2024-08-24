import asyncio
from src.bot import bot, dp
from src.handlers.common import router
from src.handlers.registration import registration_router
from src.handlers.account import account_router
from src.handlers.settings import settings_router
from src.handlers.faq import faq_router
from src.handlers.catalog import catalog_router
from src.keyboards.set_menu import set_main_menu
from src.database.models import async_main
from src.handlers.cart import cart_router
from src.handlers.help_cmd import help_router
from src.dialogs.Catalog.catalog_dialogs import Catalog
from src.dialogs.Cart.cart_dialogs import Cart
from aiogram_dialog import setup_dialogs
from src.handlers.order import order_router

from src.utils.config_funcs import names_2_routers

from ConfigFromJsonToDict import config_data

router_names = config_data['routers']

async def main():
    await async_main()
    routers = names_2_routers(router_names)
    for router in routers:
        dp.include_router(router)
    setup_dialogs(dp)
    await set_main_menu(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
