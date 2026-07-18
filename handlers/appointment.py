from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from config import SERVICES, MASTERS, TIME_SLOTS
from database import save_appointment
from handlers.common import main_keyboard

router = Router()


class AppointmentFSM(StatesGroup):
    choose_service = State()
    choose_master = State()
    choose_date_time = State()
    confirm = State()


def service_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=s)] for s in SERVICES]
        + [[KeyboardButton(text="Отмена")]],
        resize_keyboard=True,
    )


def master_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=m)] for m in MASTERS]
        + [[KeyboardButton(text="Отмена")]],
        resize_keyboard=True,
    )


def time_keyboard():
    buttons = []
    row = []
    for i, slot in enumerate(TIME_SLOTS, 1):
        row.append(KeyboardButton(text=slot))
        if i % 3 == 0:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([KeyboardButton(text="Отмена")])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


@router.message(F.text == "Записаться")
async def start_appointment(message: Message, state: FSMContext):
    await state.set_state(AppointmentFSM.choose_service)
    await message.answer(
        "Выберите услугу:",
        reply_markup=service_keyboard(),
    )


@router.message(AppointmentFSM.choose_service, F.text != "Отмена")
async def choose_service(message: Message, state: FSMContext):
    if message.text not in SERVICES:
        await message.answer("Пожалуйста, выберите услугу из меню.")
        return
    await state.update_data(service=message.text)
    await state.set_state(AppointmentFSM.choose_master)
    await message.answer(
        "Выберите мастера:",
        reply_markup=master_keyboard(),
    )


@router.message(AppointmentFSM.choose_master, F.text != "Отмена")
async def choose_master(message: Message, state: FSMContext):
    if message.text not in MASTERS:
        await message.answer("Пожалуйста, выберите мастера из меню.")
        return
    await state.update_data(master=message.text)
    await state.set_state(AppointmentFSM.choose_date_time)
    await message.answer(
        "Выберите удобное время:",
        reply_markup=time_keyboard(),
    )


@router.message(AppointmentFSM.choose_date_time, F.text != "Отмена")
async def choose_date_time(message: Message, state: FSMContext):
    if message.text not in TIME_SLOTS:
        await message.answer("Пожалуйста, выберите время из меню.")
        return
    await state.update_data(date_time=message.text)
    data = await state.get_data()
    service = data["service"]
    master = data["master"]
    date_time = data["date_time"]
    text = (
        f"📋 Проверьте данные записи:\n\n"
        f"Услуга: {service} — {SERVICES[service]}\n"
        f"Мастер: {MASTERS[master]}\n"
        f"Время: {date_time}\n\n"
        f"Всё верно?"
    )
    await state.set_state(AppointmentFSM.confirm)
    await message.answer(
        text,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Подтвердить")],
                [KeyboardButton(text="Отмена")],
            ],
            resize_keyboard=True,
        ),
    )


@router.message(AppointmentFSM.confirm, F.text == "Подтвердить")
async def confirm_appointment(message: Message, state: FSMContext):
    data = await state.get_data()
    save_appointment(
        user_id=message.from_user.id,
        username=message.from_user.username,
        service=data["service"],
        master=data["master"],
        date_time=data["date_time"],
    )
    await state.clear()
    await message.answer(
        "✅ Запись успешно создана! Ждём вас в назначенное время.",
        reply_markup=main_keyboard(),
    )


@router.message(F.text == "Отмена")
async def cancel(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
    await message.answer("Действие отменено.", reply_markup=main_keyboard())
