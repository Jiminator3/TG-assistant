import asyncio
from create_bot import bot, dp, scheduler
from handlers.cmd import cmd
from handlers.run_app import run_app
from handlers.start import start_router
from aiogram.types import BotCommand, BotCommandScopeDefault
# from work_time.time_func import send_time_msg

async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()
    dp.include_router(start_router)
    dp.include_router(run_app)
    dp.include_router(cmd)
    await set_commands()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def set_commands():
    commands = [BotCommand(command='start', description='Старт'),
                BotCommand(command='start_2', description='Старт 2'),
                BotCommand(command='start_3', description='Старт 3'),
                BotCommand(command='dota', description='Запуск доты'),
                BotCommand(command='faq', description='Частые вопросы'),
                BotCommand(command='steam', description='Открыть стим')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


if __name__ == "__main__":
    asyncio.run(main())

# TODO(Запусти море воров,
#  Прими игру(Принимает игру в доте),
#  Где моя мышка,
#  Скриншот, нужно чтобы скринило даже приложения)
#  Бюджет ( Список что нужно оплатить, может подключить банки к телеге)