from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

def start_menu():
    kb = InlineKeyboardMarkup(row_width=1, 
    inline_keyboard=[
    [InlineKeyboardButton(text='🎓 Профиль', callback_data='start|profile')],
    [InlineKeyboardButton(text='Обучение', web_app=WebAppInfo(url="https://academywebapp-kriswis.amvera.io/"))],
    [InlineKeyboardButton(text='❓ FAQ', callback_data='start|faq'), 
    InlineKeyboardButton(text='👨‍💻 Поддержка', callback_data='start|support')]])

    return kb

def cancel_operation():
    kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Меню', callback_data='start_menu')]])

    return kb


def backTo_mainMenu_kb():
    kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='↩️ Назад', callback_data='start_menu')]])

    return kb