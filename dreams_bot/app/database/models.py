# app/database/models.py
from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    gender: Mapped[str] = mapped_column(String(1), nullable=True)  # M или F
    age: Mapped[int] = mapped_column(nullable=True)
    weight: Mapped[int] = mapped_column(nullable=True)
    diseases: Mapped[str] = mapped_column(String(200), nullable=True)
    is_registered: Mapped[bool] = mapped_column(default=False)

class SleepCategory(Base):
    __tablename__ = 'sleep_categories'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

class SleepContent(Base):
    __tablename__ = 'sleep_content'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(200))
    video_link: Mapped[str] = mapped_column(String(100))
    category_id: Mapped[int] = mapped_column(ForeignKey('sleep_categories.id'))

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)