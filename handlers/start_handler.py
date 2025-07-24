import asyncio
from datetime import datetime
import logging
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from admins import get_all_admins
from bd.answers_users_comm import create_answer_data_bd, create_answer_from_user, get_data_answer_from_user, select_answer
from bd.users_commands import create_user, make_active_user, make_deactivate_user, select_user
from keyboards.inline_get_lesson import get_keyb_get_stars, get_star_data
from state.answer_state import CreateAnswer

start_message1 = f'Добро пожаловать в уютное кафе «Почему хлеб»!\nМы искренне рады видеть вас среди наших гостей.\nНадеемся, что наша душевная атмосфера, ароматный хлеб, приготовленный по особым рецептам, и внимательное обслуживание оставили у вас только приятные впечатления. Мы ценим каждого гостя и стремимся сделать ваш визит особенным.\nБудем рады видеть вас снова!'

start_message2 = 'Поставьте вашу оценку от 1 до 5.\n\n'

start_message3 = 'Благодарим за то, что поделились своими впечатлениями! Ваше мнение — это то, что помогает нам становиться ещё лучше.\n' \
    'Будем признательны, если вы оставите свой комментарий или пожелание по работе нашего кафе. Сделать это можно:\n' \
    '•в текстовом сообщении\n' \
    '•в голосовом сообщении\n' \
    '• прикрепив фото \n' \
    'Ждём ваших отзывов! Они помогают нам становиться лучше для вас 🥐'

def register_start_handlers(dp: Dispatcher):
    @dp.message_handler(commands='start')
    async def start_comm(message: types.Message):
        id_user = message.from_user.id
        first_name = message.from_user.first_name
        user_name = message.from_user.username
        logging.info(f'{id_user} ({first_name}) --> Вошел в чат')
        if select_user(id_user):
            make_active_user(id_user)
        else:
            create_user(id=id_user, first_name=first_name, user_name=user_name) 
        # if id_user in get_all_admins():
        #     await message.answer('Вы в этом боте администратор')
        # else:
        await message.answer(start_message1)
        await message.answer(start_message2, reply_markup=get_keyb_get_stars())

    # @dp.callback_query_handler()
    # async def answ_first(call: types.CallbackQuery, ):
    #     await call.answer()
    #     await call.message.delete()
    #     # await call.message.answer(start_message2)
    #     await call.message.answer(start_message2, reply_markup=get_keyb_get_stars())

    @dp.callback_query_handler(get_star_data.filter())
    async def answ_first(call: types.CallbackQuery, callback_data, state: FSMContext):
        await call.answer()
        user_id = call.from_user.id

        stars = callback_data['star']

        text_new2 = f'<b>Ваша оценка:</b> {stars}⭐️\n\n'

        await call.message.delete()
        await call.message.answer(text_new2 + start_message3)
        answer_id = create_answer_from_user(user_id, stars)
        await state.set_state(CreateAnswer.get_data)
        await state.update_data(answer_id=answer_id)
        await asyncio.sleep(900)
        if await state.get_state():
            await state.finish()
            await call.message.answer('Благодарим. \nХорошего дня!\n\nЕсли захотите написать новый отзыв, нажмите /start')
            await dp.bot.send_message(354585871, 'ПОСМОТРИ ТАМ СОСТОЯНИЕ ЗАКРЫЛОСЬ, ЕСТЬ ЛИ ОТВЕТ')
            answer_data = get_data_answer_from_user(answer_id)
            answer_info = select_answer(answer_id)
            user_data = select_user(user_id)
            msg_star_place = f"<b>Оценка:</b> {answer_info['stars']}⭐️"
            if answer_data:
                for admin in get_all_admins():
                    try:
                        await dp.bot.send_message(admin, f'✅Новый отзыв!\n\nОт: {user_data["first_name"]}\n@{user_data["user_name"]}\n\n' \
                            f'{msg_star_place}')
                        for ell in answer_data:
                                if ell['text']:
                                    await dp.bot.send_message(admin, ell['text'])
                                elif ell['voice_id']:
                                    await dp.bot.send_voice(admin, ell['voice_id'])
                                elif ell['photo_id']:
                                    await dp.bot.send_photo(admin, photo=ell['photo_id'])
                                elif ell['video_id']:
                                    await dp.bot.send_video(admin, video=ell['video_id'])
                                elif ell['sticker_id']:
                                    await dp.bot.send_sticker(admin, ell['sticker_id'])
                                elif ell['gif_id']:
                                    await dp.bot.send_animation(admin, ell['gif_id'])
                                elif ell['document_id']:
                                    await dp.bot.send_document(admin, ell['document_id'])
                                elif ell['video_note_id']:
                                    await dp.bot.send_video_note(admin, ell['video_note_id'])
                                await asyncio.sleep(1)
                        logging.info(f'{admin} - Отправили отзыв')
                    except:
                        logging.info(f'{admin} - block BOT^ not send message')

    # @dp.message_handler(state=CreateAnswer.get_data())
    # async def start_comm(message: types.Message, state: FSMContext):
    #     state_data = await state.get_data()
    #     if state_data:
    #         answer_id = state_data['answer_id']


    @dp.message_handler(content_types=[types.ContentType.ANY], state=CreateAnswer.get_data)
    async def get_answer(message: types.Message, state: FSMContext):
        keyb = types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(
            text='✅Готово, отправить отзыв', callback_data='done_answer'))
        state_data = await state.get_data()
        # print(state_data)
        answer_id = int(state_data['answer_id'])
        if message.text:
            text = message.parse_entities()
            create_answer_data_bd(answers_users_id=answer_id, text=text)
            logging.info(f'{message.from_user.id} - написал {message.text}')
        elif message.photo:
            photo_id = message.photo[-1]['file_id']
            create_answer_data_bd(
                answers_users_id=answer_id, photo_id=photo_id)
        elif message.document:
            document_id = message.document.file_id
            create_answer_data_bd(
                answers_users_id=answer_id, document_id=document_id)
        elif message.sticker:
            sticker_id = message.sticker.file_id
            create_answer_data_bd(
                answers_users_id=answer_id, sticker_id=sticker_id)
        elif message.voice:
            voice_id = message.voice.file_id
            create_answer_data_bd(
                answers_users_id=answer_id, voice_id=voice_id)
        elif message.video:
            video_id = message.video.file_id
            create_answer_data_bd(
                answers_users_id=answer_id, video_id=video_id)
        elif message.animation:
            gif_id = message.animation.file_id
            create_answer_data_bd(
                answers_users_id=answer_id, gif_id=gif_id)
        elif message.video_note:
            video_note_id = message.video_note.file_id
            create_answer_data_bd(
                answers_users_id=answer_id, video_note_id=video_note_id)

        if 'mess_id' in state_data and 'chat_id' in state_data:
            msg_id = state_data['mess_id']
            chat_id = state_data['chat_id']
            await dp.bot.delete_message(message_id=msg_id, chat_id=chat_id)
        msg = await message.answer('Если Вы написали весь отзыв, нажмите на кнопку ниже.\n\n' \
            'Если хотите еще что-то добавить, просто отправляйте сообщения в чат.', reply_markup=keyb)
        await state.update_data(mess_id=msg['message_id'], chat_id=msg.chat['id'])


    @dp.callback_query_handler(text='done_answer', state=CreateAnswer.get_data)
    async def answer_done(call: types.CallbackQuery, state: FSMContext):
        await call.answer()
        state_data = await state.get_data()
        user_id=call.from_user.id
        await state.finish()
        if 'mess_id' in state_data and 'chat_id' in state_data:
            msg_id = state_data['mess_id']
            chat_id = state_data['chat_id']
            await dp.bot.delete_message(message_id=msg_id, chat_id=chat_id)

        answer_id = int(state_data['answer_id'])
        await call.message.answer('Благодарим. \nХорошего дня!\n\nЕсли захотите написать новый отзыв, нажмите /start')
        answer_data = get_data_answer_from_user(answer_id)
        answer_info = select_answer(answer_id)
        user_data = select_user(user_id)
        msg_star_place = f"<b>Оценка:</b> {answer_info['stars']}⭐️"
        for admin in get_all_admins():
            try:
                await dp.bot.send_message(admin, f'✅Новый отзыв!\n\nОт: {user_data["first_name"]}\n@{user_data["user_name"]}\n\n' \
                    f'{msg_star_place}')
                for ell in answer_data:
                        if ell['text']:
                            await dp.bot.send_message(admin, ell['text'])
                        elif ell['voice_id']:
                            await dp.bot.send_voice(admin, ell['voice_id'])
                        elif ell['photo_id']:
                            await dp.bot.send_photo(admin, photo=ell['photo_id'])
                        elif ell['video_id']:
                            await dp.bot.send_video(admin, video=ell['video_id'])
                        elif ell['sticker_id']:
                            await dp.bot.send_sticker(admin, ell['sticker_id'])
                        elif ell['gif_id']:
                            await dp.bot.send_animation(admin, ell['gif_id'])
                        elif ell['document_id']:
                            await dp.bot.send_document(admin, ell['document_id'])
                        elif ell['video_note_id']:
                            await dp.bot.send_video_note(admin, ell['video_note_id'])
                        await asyncio.sleep(1)
                logging.info(f'{admin} - Отправили отзыв')
            except:
                logging.info(f'{admin} - block BOT, not send message')



    # Обрабатывает выход из бота
    @dp.my_chat_member_handler(run_task=True)
    async def some_handler(my_chat_member: types.ChatMemberUpdated):
        '''Обрабатывает выход пользователя из чата'''
        user_id = my_chat_member['chat']['id']
        logging.info(f'{user_id} --> Покинул бота')
        if my_chat_member['new_chat_member']['status'] == "kicked":
            make_deactivate_user(user_id)

    