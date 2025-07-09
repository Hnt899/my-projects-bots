#тут клавы 
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Настройка Тренировок')],
        [KeyboardButton(text='Настройка питания')],
        [KeyboardButton(text='Связаться с админом')],
        [KeyboardButton(text='Какие есть команды')]
    ],
    resize_keyboard=True
)

nutrition_types = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🍎 Сбалансированное', callback_data='nutrition_balanced')],
        [InlineKeyboardButton(text='🥑 Кето', callback_data='nutrition_keto')],
        [InlineKeyboardButton(text='🌱 Веганское', callback_data='nutrition_vegan')],
        [InlineKeyboardButton(text='💪 Высокобелковое', callback_data='nutrition_highprotein')],
        [InlineKeyboardButton(text='🥦 Низкоуглеводное', callback_data='nutrition_lowcarb')]
    ]
)