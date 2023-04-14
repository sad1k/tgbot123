from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"RUS: Добро пожаловать, это бот для конвертации аудио в текст! Для конвертации пришлите аудио или запишите его\n\n\nENG: Welcome, this is a bot for converting audio to text! To convert, send audio or record it")
