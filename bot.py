from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN", "BOT TOKEN СЮДА")

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

WEBAPP_URL = "https://6bc3-185-77-216-6.ngrok-free.app"  # вставь свой актуальный адрес

@dp.message(Command("start"))
async def cmd_start(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Пройти тест", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    await message.answer("Нажми на кнопку ниже, чтобы пройти тест:", reply_markup=kb)

@dp.message(F.web_app_data)
async def receive_webapp_data(message: Message):
    await message.answer(f"✅ WebApp прислал данные: {message.web_app_data.data}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
