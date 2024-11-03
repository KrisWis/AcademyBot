from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start_menu():
    kb = InlineKeyboardMarkup(row_width=1, 
    inline_keyboard=[
    [InlineKeyboardButton(text='🎓 Профиль', callback_data='start|profile')],
    [InlineKeyboardButton(text='Обучение', callback_data='start|teaching')],
    [InlineKeyboardButton(text='❓ FAQ', callback_data='start|faq'), 
    InlineKeyboardButton(text='👨‍💻 Поддержка', callback_data='start|support')]])

    return kb

def cancel_operation():
    kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Меню', callback_data='start_menu')]])

    return kb