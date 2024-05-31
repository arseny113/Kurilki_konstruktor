from src.utils.funcs import get_image_ratio, get_image_size
from src.database.models import async_session, User, Catalog, Order
from sqlalchemy import select, delete


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def check_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            return False
        else:
            return True


async def update_name_phone_email(tg_id, **kwargs):
    async with async_session() as session:
        user_id = await session.scalar(select(User.id).where(User.tg_id == tg_id))
        user = await session.get(User, user_id)
        for data_type, data in kwargs.items():
            if data_type == 'name':
                user.name = data
            if data_type == 'phone':
                user.phone = data
            if data_type == 'email':
                user.email = data
            await session.commit()


async def get_name(tg_id):
    async with async_session() as session:
        name = await session.scalar(select(User.name).where(User.tg_id == tg_id))
        return name


async def get_number(tg_id):
    async with async_session() as session:
        phone = await session.scalar(select(User.phone).where(User.tg_id == tg_id))
        return phone


async def get_email(tg_id):
    async with async_session() as session:
        email = await session.scalar(select(User.email).where(User.tg_id == tg_id))
        return email


async def get_orders(tg_id):
    async with async_session() as session:
        query = select(Order.prod_id, Order.amount).where(Order.tg_id == tg_id)
        result = await session.execute(query)
        return result.scalars().all()

async def write_to_order(tg_id, product, quant):
    async with async_session() as session:
        order = await session.get(Order, tg_id)
        if order:
            order.prod_id = product
            order.amount = quant
        else:
            session.add(Order(tg_id=tg_id, prod_id=product, amount=quant))
        session.commit()

async def get_products(prod_id):
    async with async_session() as session:
        query = select(Catalog.brand, Catalog.puffs, Catalog.flavor).where(Catalog.id == prod_id)
        result = await session.execute(query)
        return result.scalars().first()
