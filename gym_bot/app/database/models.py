#тут костяк бд
from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')  # если нет бд то создаёт

async_session = async_sessionmaker(engine)

from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

class Base(AsyncAttrs, DeclarativeBase): #создаём базу мамочку всех наших остольных баз(она дочерка AsyncAttrs, DeclarativeBase)
    pass
#1
class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    gender: Mapped[str] = mapped_column(String(1), nullable=True)  # м или ж
    height: Mapped[int] = mapped_column(nullable=True)  # в см
    weight: Mapped[int] = mapped_column(nullable=True)  # в кг
    is_registered: Mapped[bool] = mapped_column(default=False)
#2
class Category(Base):
    __tablename__ = 'categories'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
#3
class Workout(Base):
    __tablename__ = 'training'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(100))
    videotraining: Mapped[str] = mapped_column(String(100))
    category: Mapped[int] = mapped_column(ForeignKey('categories.id'))

#Выгрузка и создание таблиц из Base.metadata по умолчанию не выполняются асинхронно, и нам нет смысла это менять. (sqlalchemy)
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)