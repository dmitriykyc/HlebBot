import logging
from dotenv import load_dotenv
from aiogram import Dispatcher, types


def register_unknown_mess_handler(dp: Dispatcher):
    @dp.message_handler(content_types=[types.ContentType.ANY])
    async def unknown_ness(message: types.Message):
        logging.info(f'☀️Неизвестное сообщение: {message}')
        await message.reply('К сожалению, я не знаю такой команды🙂\n\nЕсли хотите отправить отзыв, нажмите /start')