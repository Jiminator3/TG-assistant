import asyncio
from subprocess import Popen

from aiogram import Router

from filters.is_admin import IsAdmin
from aiogram.filters import Command
from aiogram.types import Message

from utils.subprocess import process_exists, processes_exist

run_app = Router()


@run_app.message(Command('steam'), IsAdmin())
async def start_steam(message: Message):
    if process_exists("steam.exe"):
        print("Стим уже запущен")
    else:
        Popen(r"F:\Steam\steam.exe")
        while not processes_exist(["SteamService.exe", "steamwebhelper.exe"]):
            await asyncio.sleep(15)
            print("Пробую запустить стим")
        await message.answer("Запустил Стим!")


@run_app.message(Command('dota'), IsAdmin())
async def start_dota(message: Message):
    if process_exists("dota2.exe"):
        print("Дота уже запущена")
    else:
        await start_steam(message)
        Popen(r"F:\Steam\steamapps\common\dota 2 beta\game\bin\win64\dota2.exe")
        await message.answer("Запустил Доту!")
