from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import *
from app.db.initdb import with_session
from sqlalchemy.orm import DeclarativeBase, DeclarativeMeta


class BaseDAO:
    """
    Base Data Access Object
    """

    __abstract__ = True
    _model = None

    @classmethod
    @with_session
    async def add_by_kwargs(cls, session: AsyncSession, **kwargs) -> "DeclarativeBase":
        """
        Adds new row with fields from kwargs.
        :param session: passed by decorator
        :param kwargs: model fields
        """
        new_instance = cls._model(**kwargs)
        session.add(new_instance)
        await session.flush()
        return new_instance

    @classmethod
    @with_session
    async def add(cls, session: AsyncSession, model_instance: DeclarativeMeta) -> DeclarativeMeta:
        """
        :param session: passed by decorator
        :param model_instance: DeclarativeMeta instance
        """
        session.add(model_instance)
        await session.flush()

        return model_instance

    @classmethod
    @with_session
    async def add_all(cls, session: AsyncSession, model_instances: list[DeclarativeMeta]) -> None:
        """
        :param session: passed by decorator
        :param model_instances: list of DeclarativeMeta instances,
        must be passed as keyword argument 'model_instances=[Instance()]'
        """
        session.add_all(model_instances)

    @classmethod
    @with_session
    async def add_if_not_exist(cls, session: AsyncSession, **kwargs) -> "DeclarativeBase":
        query = select(cls._model)
        for k, v in kwargs.items():
            query = query.where(getattr(cls._model, k) == v)
        result = await session.scalars(query)
        ins = result.one_or_none()
        if ins:
            return ins
        new_ins = cls._model(**kwargs)
        session.add(new_ins)
        await session.flush()
        return new_ins

    @classmethod
    @with_session
    async def get_all_by_kwargs(cls, session: AsyncSession, **kwargs) -> list["DeclarativeBase"]:
        """
        Get all rows filtered by kwargs where key is field name, value is field value matched with AND operator.

        e.g. get_all_by_kwargs(id=12, name='Jhon') - returns all rows where id=12 and name='Jhon'

        e.g. get_all_by_kwargs() - returns all rows

        :param session: passed by decorator
        :param kwargs: model fields
        """
        query = select(cls._model)
        for k, v in kwargs.items():
            query = query.where(getattr(cls._model, k) == v)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    @with_session
    async def update_by_id(cls, session: AsyncSession, id_: int, **kwargs):
        '''id field mandatory'''
        query = select(cls._model).where(cls._model.id == id_)
        result = await session.scalars(query)
        instance = result.first()
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            await session.flush()
            return instance
        return None

    @classmethod
    @with_session
    async def get_one_or_none(cls, session: AsyncSession, **kwargs) -> "DeclarativeBase":
        """
        Get row filtered by kwargs where key is field name, value is field value.

        e.g. get_one_or_none(id=12, name='Jhon') - returns a row where id=12 and name='Jhon' if exists

        :param session: passed by decorator
        :param kwargs: model fields
        """
        query = select(cls._model)
        for k, v in kwargs.items():
            query = query.where(getattr(cls._model, k) == v)
        result = await session.execute(query)
        return result.scalars().one_or_none()

    @classmethod
    @with_session
    async def delete_many(cls, session: AsyncSession, model_instances: list[DeclarativeMeta]) -> None:
        """
        :param session: passed by decorator
        :param model_instances: list of DeclarativeMeta instances, must be passed as keyword argument
        'model_instances=[Instance(),]'
        """
        for instance in model_instances:
            await session.delete(instance)

    @classmethod
    @with_session
    async def delete_all_by_filter(cls, session: AsyncSession, **kwargs) -> None:
        """
        Deletes rows filtered by kwargs where key is field name, value is field value.

        e.g. delete_all_by_filter(id=12, name='Jhon') - deletes all rows where id=12 and name='Jhon'

        e.g. delete_all_by_filter() - deletes all rows

        :param session: passed by decorator
        :param kwargs: model fields
        """
        query = select(cls._model)
        for k, v in kwargs.items():
            query = query.where(getattr(cls._model, k) == v)
        result = await session.execute(query)
        for instance in result.scalars().all():
            await session.delete(instance)

