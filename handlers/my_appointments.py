from aiogram import Router, F
from aiogram.types import Message

from database import get_user_appointments
from handlers.common import main_keyboard

router = Router()


@router.message(F.text == "Мои записи")
async def my_appointments(message: Message):
    rows = get_user_appointments(message.from_user.id)
    if not rows:
        await message.answer(
            "У вас пока нет активных записей.",
            reply_markup=main_keyboard(),
        )
        return
    text_lines = []
    for row in rows:
        text_lines.append(
            f"• {row['service']} | {row['master']} | {row['date_time']}"
        )
    await message.answer(
        "📅 Ваши записи:\n\n" + "\n".join(text_lines),
        reply_markup=main_keyboard(),
    )
