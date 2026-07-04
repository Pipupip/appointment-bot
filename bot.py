import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from database import init_db
from handlers import common, appointment, my_appointments

logging.basicConfig(level=logging.INFO)


async def main():
    init_db()

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()

    dp.include_router(common.router)
    dp.include_router(appointment.router)
    dp.include_router(my_appointments.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
