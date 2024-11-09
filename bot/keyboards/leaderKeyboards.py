
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def stats_kb():
    kb = InlineKeyboardMarkup(row_width=4, inline_keyboard=[
        [InlineKeyboardButton(text='День', callback_data='stats|day'),
        InlineKeyboardButton(text='Неделя', callback_data='stats|week'),
        InlineKeyboardButton(text='Месяц', callback_data='stats|month'),
        InlineKeyboardButton(text='Все время', callback_data='stats|all')],
        [InlineKeyboardButton(text='Вернуться в меню', callback_data='start_menu')]])
    
    return kb