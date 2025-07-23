from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
 

get_star_data = CallbackData('get_stars', 'star')

def get_keyb_get_stars():
    keyboard = InlineKeyboardMarkup(row_width=5)
    but = InlineKeyboardButton(text='1⭐️', 
        callback_data=get_star_data.new(star=1))
    but2 = InlineKeyboardButton(text='2⭐️', 
        callback_data=get_star_data.new(star=2))
    but3 = InlineKeyboardButton(text='3⭐️', 
        callback_data=get_star_data.new(star=3))
    but4 = InlineKeyboardButton(text='4⭐️', 
        callback_data=get_star_data.new(star=4))
    but5 = InlineKeyboardButton(text='5⭐️', 
        callback_data=get_star_data.new(star=5))
    keyboard.add(but, but2, but3, but4, but5)

    return keyboard