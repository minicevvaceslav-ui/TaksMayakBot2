import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Text, CommandStart
from aiogram.types import KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv

# Загружаем переменные окружения (токен)
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Константы с текстами и ссылками ---
LINK_DRIVER = "https://forms.fleet.yandex.ru/forms?specification=taxi&ref_id=b21aa999243246e0ae39d1e7885f784a"
LINK_SELF_EMPLOYED = "https://forms.fleet.yandex.ru/forms?specification=taxi&ref_id=a0f9f5e2e0484f569640ea686f1b813e"
LINK_IP = "https://forms.fleet.yandex.ru/forms?specification=taxi&ref_id=f3c3a48428224cfc9bdc30a6534c24d1"

INSTRUCTION_SELF_EMPLOYED = (
    "<b>Как оформить самозанятость?</b>\n\n"
    "Регистрация занимает 5-10 минут. Что нужно сделать:\n\n"
    "1. Скачайте приложение «Мой налог».\n"
    "2. Укажите номер телефона и подтвердите его по SMS.\n"
    "3. Выберите регион деятельности.\n"
    "4. Отсканируйте паспорт.\n"
    "5. Сделайте селфи по инструкции.\n"
    "6. Подтвердите регистрацию.\n\n"
    "Готово! Если смартфона нет, используйте веб-версию на сайте ФНС."
)
MANAGER_CONTACT = "+79216877780 — Контакт таксопарка Маяк"
WELCOME_TEXT = (
    "Привет! Это бот-помощник таксопарка «Маяк».\n\n"
    "Здесь вы можете быстро и самостоятельно зарегистрироваться водителем и начать зарабатывать. "
    "Выберите подходящий вариант ниже."
)

# --- Создание клавиатуры ---
def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Подключиться как парковый водитель"))
    builder.row(KeyboardButton(text="Подключиться как парковый самозанятый"))
    builder.row(KeyboardButton(text="Подключиться как парковый ИП"))
    builder.row(KeyboardButton(text="Помощь в оформлении самозанятости"))
    builder.row(KeyboardButton(text="Связаться с менеджером"))
    return builder.as_markup(resize_keyboard=True)

# --- Обработчики сообщений ---
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(WELCOME_TEXT, reply_markup=get_main_keyboard())

@dp.message(Text(text="Подключиться как парковый водитель"))
async def handle_driver(message: types.Message):
    await message.answer(
        "Отлично! Чтобы подключиться как парковый водитель, заполните анкету по ссылке:",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(LINK_DRIVER, disable_web_page_preview=True)

@dp.message(Text(text="Подключиться как парковый самозанятый"))
async def handle_self_employed(message: types.Message):
    await message.answer(
        "Чтобы подключиться как самозанятый, перейдите по ссылке:",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(LINK_SELF_EMPLOYED, disable_web_page_preview=True)
    await message.answer(INSTRUCTION_SELF_EMPLOYED, parse_mode='HTML')

@dp.message(Text(text="Подключиться как парковый ИП"))
async def handle_ip(message: types.Message):
    await message.answer(
        "Чтобы подключиться как ИП, заполните форму по ссылке:",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(LINK_IP, disable_web_page_preview=True)

@dp.message(Text(text="Помощь в оформлении самозанятости"))
async def handle_help_self(message: types.Message):
    await message.answer(INSTRUCTION_SELF_EMPLOYED, parse_mode='HTML')

@dp.message(Text(text="Связаться с менеджером"))
async def contact_manager(message: types.Message):
    await message.answer(f"Вы можете связаться с нами по номеру:\n{MANAGER_CONTACT}")

# --- Основная функция запуска ---
async def main():
    # Проверяем, что токен существует
    if not BOT_TOKEN:
        logging.critical("Ошибка: BOT_TOKEN не найден. Проверьте переменные окружения.")
        return

    logging.info("Бот запускается...")
    await dp.start_polling(bot)

if name == "__main__":
    asyncio.run(main())
