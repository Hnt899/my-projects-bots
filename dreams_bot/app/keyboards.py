# app/keyboards.py
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Видео для улучшения сна')],
        [KeyboardButton(text='Виды сна')],
        [KeyboardButton(text='Связаться с админом')],
        [KeyboardButton(text='Ложусь спать')],
        [KeyboardButton(text='Какие есть команды')]
    ],
    resize_keyboard=True
)