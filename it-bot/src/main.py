from app.create_bot import bot, dp
import asyncio

from app.stages.stageadmin import register_stageadmin
from app.stages.stagedriver import register_driver_handlers
from app.stages.stagelogist import register_logist_handlers
from app.stages.start import register_handlers_start

async def async_main():
    register_stageadmin(dp)
    register_driver_handlers(dp)
    register_handlers_start(dp)
    register_logist_handlers(dp)
    try: 
        await dp.start_polling(bot)
    except Exception as e:
        print(e)
    finally:
        print("The end.")
def main():
    asyncio.run(async_main())

if __name__ == "__main__":
    main()