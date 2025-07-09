# main.py
import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.database.models import async_main

async def main():
    await async_main()
    bot = Bot(token='7859641531:AAHG-OMSfH-4BAFflzSEv1isPa4C2IQOfOc')  # Замените на ваш токен
    dp = Dispatcher()
    dp.include_router(router)
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped')