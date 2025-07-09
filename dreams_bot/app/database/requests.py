# app/database/requests.py
from app.database.models import async_session
from app.database.models import User, SleepCategory, SleepContent
from sqlalchemy import select

async def get_user(tg_id: int) -> User:
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))

async def create_or_update_user(tg_id: int, gender: str, age: int, weight: int, diseases: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.gender = gender
            user.age = age
            user.weight = weight
            user.diseases = diseases
            user.is_registered = True
        else:
            session.add(User(
                tg_id=tg_id,
                gender=gender,
                age=age,
                weight=weight,
                diseases=diseases,
                is_registered=True
            ))
        await session.commit()

async def get_sleep_categories():
    async with async_session() as session:
        return await session.scalars(select(SleepCategory))

async def get_sleep_content(category_id):
    async with async_session() as session:
        return await session.scalars(select(SleepContent).where(SleepContent.category_id == category_id))

async def get_content(content_id):
    async with async_session() as session:
        return await session.scalar(select(SleepContent).where(SleepContent.id == content_id))