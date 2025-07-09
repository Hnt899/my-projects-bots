from app.db.models import *
from app.db.dao import *

class UserDAO(BaseDAO):
    _model = User

class TripDAO(BaseDAO):
    _model = Trip
    @classmethod
    @with_session
    async def get_sum_by_kwargs(cls, session: AsyncSession, **kwargs) -> list["DeclarativeBase"]:
        """
        Get all rows filtered by kwargs where key is field name, value is field value matched with AND operator.

        e.g. get_all_by_kwargs(id=12, name='Jhon') - returns all rows where id=12 and name='Jhon'

        e.g. get_all_by_kwargs() - returns all rows

        :param session: passed by decorator
        :param kwargs: model fields
        """
        query = select(func.sum(cls._model.cost)).group_by(cls._model.chat_id)
        for k, v in kwargs.items():
            query = query.where(getattr(cls._model, k) == v)
        result = await session.execute(query)
        return result.scalar()
    
    


