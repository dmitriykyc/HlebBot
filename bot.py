import asyncio
import os
import logging

from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.contrib.fsm_storage.redis import RedisStorage2
from dotenv import load_dotenv
from aiogram import Dispatcher, Bot, types
from handlers.start_handler import register_start_handlers
from handlers.unicnown_mess import register_unknown_mess_handler


load_dotenv()
logging.basicConfig(level=logging.INFO, filename="3dsMaxBot.log",
                    format=":--> %(asctime)s %(levelname)s %(message)s")

def register_all_middlewares(dp):
    pass


def register_all_filters(dp):
    pass


def register_all_handlers(dp):
    register_start_handlers(dp)
    register_unknown_mess_handler(dp)

async def main():
    bot = Bot(token=os.getenv("TOKEN"), parse_mode='HTML')
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)
    await dp.bot.send_message(354585871, 'Stolovaya Bot')

    # start
    try:
        logging.info('Bot srarted')
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped!")