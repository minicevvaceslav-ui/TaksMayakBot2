import logging
import os
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from dotenv import load_dotenv

# --- Инициализация ---
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)

# Критическая проверка токена перед запуском
if not BOT_TOKEN:
    logging.critical("CRITICAL ERROR: BOT_TOKEN is not set in environment variables!")
    exit()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# --- Константы ---
# Ссылка для паркового водителя больше не нужна
# LINK_DRIVER = "https://forms.fleet.yandex.ru/forms?specification=taxi&ref_id=b21aa999243246e0ae39d1e7885f784a"
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

# --- Клавиатура (синтаксис для v2) ---
# Убрали кнопку "Подключиться как парковый водитель"
btn_self = KeyboardButton("Подключиться как парковый самозанятый")
btn_ip = KeyboardButton("Подключиться как парковый ИП")
btn_help = KeyboardButton("Помощь в оформлении самозанятости")
btn_manager = KeyboardButton("Связаться с менеджером")

# Убрали кнопку из самой клавиатуры
main_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_self).add(btn_ip).add(btn_help).add(btn_manager)

# --- Обработчики команд (синтаксис для v2) ---
@dp.message_handler(commands=['start', 'help'])
async def cmd_start(message: types.Message):
    await message.answer(WELCOME_TEXT, reply_markup=main_kb)

# Убрали обработчик для кнопки "Подключиться как парковый водитель"

@dp.message_handler(lambda message: message.text == "Подключиться как парковый самозанятый")
async def handle_self_employed(message: types.Message):
    await message.answer("Чтобы подключиться как самозанятый, перейдите по ссылке:", reply_markup=ReplyKeyboardRemove())
    await message.answer(LINK_SELF_EMPLOYED, disable_web_page_preview=True)
    await message.answer(INSTRUCTION_SELF_EMPLOYED, parse_mode='HTML')

@dp.message_handler(lambda message: message.text == "Подключиться как парковый ИП")
async def handle_ip(message: types.Message):
    await message.answer("Чтобы подключиться как ИП, заполните форму по ссылке:", reply_markup=ReplyKeyboardRemove())
    await message.answer(LINK_IP, disable_web_page_preview=True)

@dp.message_handler(lambda message: message.text == "Помощь в оформлении самозанятости")
async def handle_help_self(message: types.Message):
    await message.answer(INSTRUCTION_SELF_EMPLOYED, parse_mode='HTML')

@dp.message_handler(lambda message: message.text == "Связаться с менеджером")
async def contact_manager(message: types.Message):
    await message.answer(f"Вы можете связаться с нами по номеру:\n{MANAGER_CONTACT}")

# --- Запуск бота (синтаксис для v2) ---
if name == "__main__":
    logging.info("Бот запускается (v2 compatible)...")
    executor.start_polling(dp, skip_updates=True)
