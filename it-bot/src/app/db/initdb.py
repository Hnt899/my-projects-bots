from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs, AsyncSession
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Table, Boolean, Float
from sqlalchemy.orm import DeclarativeBase, declared_attr
# TODO Write necessary database name
db_name="database"
DATABASE_URL = f"sqlite+aiosqlite:///./{db_name}.db"
engine = create_async_engine(url=DATABASE_URL)
from collections.abc import Callable
from functools import wraps
from typing import Any
from loguru import logger

async_session_factory = async_sessionmaker(create_async_engine(DATABASE_URL), class_=AsyncSession, expire_on_commit=False)
def with_session(func_: Callable) -> Callable:
    """
    Async session factory.
    """

    @wraps(func_)
    async def wrapper(*args, **kwargs) -> Any:
        async with async_session_factory() as session:
            try:
                result = await func_(*args, session=session, **kwargs)
                await session.commit()
                return result
            except Exception as exc:
                await session.rollback()
                logger.exception(f"Error executing DB operation: {exc!r}",   exc_info=exc)
                return None
            finally:
                await session.close()

    return wrapper



class AsyncBase(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()+'s'
