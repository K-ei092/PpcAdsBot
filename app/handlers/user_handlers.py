# import os
# from difflib import get_close_matches
#
# from aiogram import F, Router
# from aiogram.filters import Command, CommandStart
# from aiogram.types import CallbackQuery, Message, FSInputFile
#
# from filters.my_filters import CheckCity
#
# from keyboards.kb import create_collect_keyboard
# from lexicon.lexicon import LEXICON
# from lexicon.city import LIST_CITY
# from database.database import users_db
# from config_data.config import Config, load_config
# from parser.parser_YA import get_file
#
#
# router = Router()
#

# # Этот хэндлер будет срабатывать на инлайн-клавиатуру выбора вида выдачи
# # и отправлять сообщение с предложением ввести ключевую фразу для поиска
# @router.callback_query(F.data.startswith('^collect^'))
# async def process_collect_command(callback: CallbackQuery):
#     user_id = callback.from_user.id
#     if callback.data[9] == '1':
#         users_db[user_id] = [1]
#     elif callback.data[9] == '2':
#         users_db[user_id] = [2]
#     elif callback.data[9] == '3':
#         users_db[user_id] = [3]
#     await callback.message.edit_text(
#         text=LEXICON['^collect^']
#     )
#
#
# # Этот хэндлер будет срабатывать на введение ключевой фразы, добавлять
# # её в базу и отправлять сообщение с предложением ввести регион поиска
# @router.message(F.text.startswith('?'))
# async def process_phrase_command(message: Message):
#     user_id = message.from_user.id
#     if users_db.get(user_id, 0):
#         users_db[user_id].append(message.text[1:])
#         await message.answer(
#             text=LEXICON['region']
#         )
#     else:
#         await message.answer(
#             text="Начните с команды /start"
#         )
#
#
# # Этот хэндлер будет срабатывать на введение региона, добавлять его в базу,
# # запрашивать парсинг и отправлять результат парсинга пользователю
# @router.message(CheckCity())
# async def process_region_command(message: Message):
#     user_id = message.from_user.id
#     if users_db.get(user_id, 0) and len(users_db[user_id]) == 2:
#         users_db[user_id].append(get_close_matches(message.text, LIST_CITY, n=1, cutoff=0.8)[0])
#         await message.answer(
#             text=LEXICON['wait'])

#         result = get_file(user_id)

#         if type(result) == str and result.endswith('.xlsx'):
#             file = FSInputFile(result)
#             await message.answer(
#                 text="Ваш результат")
#             await message.answer_document(file)
#             os.remove(result)
#         else:
#             await message.answer(
#                 text="Сервер не дал ответа, попробуйте ещё"
#             )
#         del users_db[user_id]
#     else:
#         await message.answer(
#             text="Нарушен порядок"
#         )