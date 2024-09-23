from urllib.parse import uses_relative

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from utils import user_simulations

automations = Router()

@automations.message(Command("mouse_coord"))
async def mouse_coord(message: Message):
    await message.answer(user_simulations.get_mouse_position())
