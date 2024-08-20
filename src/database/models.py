from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from src.data.config import database_url
from ConfigFromJsonToDict import config_data
import pandas as pd
import csv


engine = create_async_engine(url=database_url, echo=True, pool_size=5, max_overflow=10)
async_session = async_sessionmaker(engine)

levels_choice_count = int(config_data['texts']['catalog']['dialog']['levels_choice_count'])

with open(r'src/database/DB_ver06.csv', encoding='UTF-8-sig') as file:
    reader = csv.reader(file, delimiter=';')
    header = list(next(reader))
    column_names = header
    all_products = []
    for row in reader:
        new_line = {k: v for k, v in zip(header, row)}
        all_products.append(new_line)
    df = pd.DataFrame(all_products)
    lvl_names = column_names[1:levels_choice_count + 1]


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)


class Catalog(Base):
    __tablename__ = 'catalog'

    id: Mapped[int] = mapped_column(primary_key=True)
    for name in column_names[1:]:
        locals()[f"{name}"]: Mapped[str] = mapped_column(String(300), nullable=True)



class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    prod_id: Mapped[int] = mapped_column(nullable=True)
    amount: Mapped[int] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=True)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    dict_for_db = {}
    async with async_session() as session:
        for index, row in df.iterrows():
            for i in range(len(column_names)):
                if i == 0:
                    dict_for_db[column_names[i]] = int(row[i])
                else:
                    dict_for_db[column_names[i]] = row[i]
            record = Catalog(**dict_for_db)

            session.add(record)

        await session.commit()

