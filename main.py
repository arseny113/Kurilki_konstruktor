import asyncio
from src.bot import bot, dp
from src.handlers.common import router
from src.handlers.settings import settings_router
from src.handlers.registration import registration_router
# from src.handlers.catalog import catalog_router
from src.database.models import async_main
# from src.handlers.orders import order_router
# from src.dialogs.Catalog.catalog_dialogs import Catalog_lvl1
from aiogram_dialog import setup_dialogs
# from src.handlers.order_registration import order_registration_router


async def main():
    await async_main()
    dp.include_router(router)
    # dp.include_router(catalog_router)
    dp.include_router(settings_router)
    dp.include_router(registration_router)
    # dp.include_router(order_router)
    # dp.include_router(order_registration_router)
    # dp.include_router(Catalog_lvl1)
    setup_dialogs(dp)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
