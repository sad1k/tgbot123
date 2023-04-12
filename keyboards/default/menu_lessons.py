from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_lessons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Математика")
        ],
        [
            KeyboardButton(text="Русский")
        ]
    ],
    resize_keyboard=True
)