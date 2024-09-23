import os
from aiogram.filters import Command, CommandObject

from aiogram import Router
from aiogram.types import Message

from filters.is_admin import IsAdmin

cmd = Router()

@cmd.message(Command("restart"), IsAdmin())
async def restart(message: Message, command: CommandObject):
    args = command.args
    if args is None:
        await message.answer("Введите через сколько минут выключить компьютер.")
        return
    seconds = int(args)*60
    await message.answer(f"Компьютер будет перезагружен через {args} минут.")
    os.system(f'shutdown /r /t {seconds}')

@cmd.message(Command("shutdown"), IsAdmin())
async def shutdown(message: Message, command: CommandObject):
    args = command.args
    if args is None:
        await message.answer("Введите через сколько минут выключить компьютер.")
        return
    seconds = int(args)*60
    await message.answer(f"Компьютер будет выключен через {args} минут.")
    os.system(f'shutdown /s /t {seconds}')

@cmd.message(Command("cancel_restart"), IsAdmin())
async def cancel_restart(message: Message):
    os.system("shutdown /a")
    await message.answer("Рестарт отменен")