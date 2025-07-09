# основной фаил проекта и тут же мы встовляем токен
import asyncio
import os
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.database.models import async_main
from pathlib import Path

async def main():
    
    await async_main()
    bot = Bot(token='7806482724:AAHM2Q-HEfUDryBEok2yysmSloEc37L-iYc') #токен
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
        print('Bot stopped') #делай нормальную остановку бота