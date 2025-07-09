#запросы в бд
from app.database.models import async_session
from app.database.models import User, Category, Workout
from sqlalchemy import select
#Получает пользователя из базы данных по его Telegram ID
async def get_user(tg_id: int) -> User:
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))
# Создает нового пользователя или обновляем существуещего
async def create_or_update_user(tg_id: int, gender: str, height: int, weight: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.gender = gender
            user.height = height
            user.weight = weight
            user.is_registered = True
        else:
            session.add(User(
                tg_id=tg_id,
                gender=gender,
                height=height,
                weight=weight,
                is_registered=True
            ))
        await session.commit()
# Получает все доступные категории тренировок.
async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))
#Получает все тренировки для указанной категории
async def get_workouts(category_id):
    async with async_session() as session:
        return await session.scalars(select(Workout).where(Workout.category == category_id))
#Получает конкретную тренировку по её ID.
async def get_workout(workout_id):
    async with async_session() as session:
        return await session.scalar(select(Workout).where(Workout.id == workout_id))