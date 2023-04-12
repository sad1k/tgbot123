from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Учитель")
        ],
        [
            KeyboardButton(text="Студент")
        ]
    ],
    resize_keyboard=True
)
