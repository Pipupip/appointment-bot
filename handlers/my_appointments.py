from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

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
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Отменить запись", callback_data="cancel_appointment")]
            ]
        ),
    )


@router.callback_query(F.data == "cancel_appointment")
async def cancel_appointment_prompt(callback: CallbackQuery):
    await callback.message.edit_text(
        "Функция отмены записи будет доступна в следующем обновлении.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Назад", callback_data="back_to_menu")]
            ]
        ),
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Главное меню:", reply_markup=main_keyboard())
    await callback.answer()
