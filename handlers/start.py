from typing import Any

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from sqlalchemy import Integer, String, TIMESTAMP

from db_handler import db_service
from filters.is_admin import IsAdmin
from keyboards.all_kb import main_kb, create_spec_kb, create_rat
from keyboards.inline_kbs import ease_link_kb, get_inline_kb, create_qst_inline_kb
from utils import get_db_options, get_db_types
from utils.user_generator import get_random_person
from aiogram.types import CallbackQuery
import asyncio
from aiogram.utils.chat_action import ChatActionSender
from create_bot import questions, bot

start_router = Router()


@start_router.message(CommandStart(), IsAdmin())
async def cmd_start(message: Message, command: CommandObject):
    command_args: str = command.args
    if command_args:
        await message.answer(
            f'Запуск сообщения по команде /start используя фильтр CommandStart() с меткой <b>{command_args}</b>',
            reply_markup=main_kb(message.from_user.id))
    else:
        await message.answer(
            f'Запуск сообщения по команде /start используя фильтр CommandStart() без метки',
            reply_markup=main_kb(message.from_user.id))


@start_router.message(Command('start_2'), IsAdmin())
async def cmd_start(message: Message):
    await message.answer('Запуск сообщения по команде /start_2 используя фильтр Command()',
                         reply_markup=create_spec_kb())


@start_router.message(F.text == '/start_3', IsAdmin())
async def cmd_start(message: Message):
    await message.answer('Запуск сообщения по команде /start_3 используя магический фильтр F.text!',
                         reply_markup=create_rat())


@start_router.message(F.text == 'Давай инлайн!', IsAdmin())
async def get_inline_btn_link(message: Message):
    await message.answer('Вот тебе инлайн клавиатура со ссылками!', reply_markup=ease_link_kb())


@start_router.message(F.text == 'Давай инлайн2', IsAdmin())
async def get_inline_btn_link(message: Message):
    await message.answer('Вот тебе инлайн клавиатура со ссылками!', reply_markup=get_inline_kb())


@start_router.callback_query(F.data == 'get_person', IsAdmin())
async def send_random_person(call: CallbackQuery):
    await call.answer('Генерирую случайного пользователя')
    user = get_random_person()
    formatted_message = (
        f"👤 <b>Имя:</b> {user['name']}\n"
        f"🏠 <b>Адрес:</b> {user['address']}\n"
        f"📧 <b>Email:</b> {user['email']}\n"
        f"📞 <b>Телефон:</b> {user['phone_number']}\n"
        f"🎂 <b>Дата рождения:</b> {user['birth_date']}\n"
        f"🏢 <b>Компания:</b> {user['company']}\n"
        f"💼 <b>Должность:</b> {user['job']}\n"
    )
    await call.message.answer(formatted_message)


@start_router.callback_query(F.data == 'back_home', IsAdmin())
async def back_home(call: CallbackQuery):
    await call.answer()
    await call.message.answer("Вы вернулись", reply_markup=main_kb(call.from_user.id))


@start_router.message(Command('faq'), IsAdmin())
async def cmd_start_2(message: Message):
    await message.answer('Сообщение с инлайн клавиатурой с вопросами', reply_markup=create_qst_inline_kb(questions))


@start_router.callback_query(F.data.startswith('qst_'), IsAdmin())
async def cmd_start(call: CallbackQuery):
    await call.answer()
    qst_id = int(call.data.replace('qst_', ''))
    qst_data = questions[qst_id]
    msg_text = f'Ответ на вопрос {qst_data.get("qst")}\n\n' \
               f'<b>{qst_data.get("answer")}</b>\n\n' \
               f'Выбери другой вопрос:'
    async with ChatActionSender(bot=bot, chat_id=call.from_user.id, action="typing"):
        await asyncio.sleep(2)
        await call.message.answer(msg_text, reply_markup=create_qst_inline_kb(questions))


@start_router.message(Command("create_table"))
async def create_table(message: Message, command: CommandObject):
    try:
        command_split = command.args.split(":")[0].split(",")
        first_options = get_db_options(command_split[1:])
        command_split[2] = get_db_types(command_split[2])
        columns = [{'name': command_split[1], 'type': command_split[2]}]
        if first_options is not None:
            columns[0].update(first_options)

        other_records = command.args.split(":")[1:]
        for record in other_records:
            record_list: list = record.split(",")
            options = get_db_options(record_list)

            record_list[1] = get_db_types(record_list[1])

            if options is not None:
                columns.append({'name': record_list[0], 'type': record_list[1] | options})
            else:
                columns.append({'name': record_list[0], 'type': record_list[1]})
        await db_service.create_table(command_split[0], columns)
        await message.answer("Таблица создалась!")
    except Exception as e:
        await message.answer(f'Таблица не создалась: {e}')


@start_router.message(Command("create_table_help"))
async def create_table_help(message: Message):
    message_text = f"Чтобы создать таблицу нужно ввести сообщение /create_table \n\n" \
                   f"C аргументами - Имя таблицы,Название колонки,Тип колонки,Доп опции:следующая строка\n\n" \
                   f"Возможные типы - Integer, String, TIMESTAMP"
    await message.answer(message_text)
