from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

router = Router()


def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Записаться")],
            [KeyboardButton(text="Мои записи")],
            [KeyboardButton(text="О нас")],
        ],
        resize_keyboard=True,
    )


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Добро пожаловать! ✂️\n\n"
        "Это бот для записи на услуги барбершопа.\n"
        "Выберите действие в меню ниже:",
        reply_markup=main_keyboard(),
    )


@router.message(F.text == "О нас")
async def about(message: Message):
    await message.answer(
        "Наш барбершоп — это место, где стиль встречается с профессионализмом.\n"
        "📍 ул. Примерная, д. 1\n"
        "🕐 Пн-Сб: 10:00 — 20:00\n"
        "📞 +7 (999) 123-45-67",
        reply_markup=main_keyboard(),
    )
