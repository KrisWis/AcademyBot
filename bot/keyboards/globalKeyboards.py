from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from utils import const

# Клавиатура стартового меню
def start_menu(user_status: str):
    kb = InlineKeyboardMarkup(row_width=1, 
    inline_keyboard=[
    [InlineKeyboardButton(text='🎓 Профиль', callback_data='start|profile')],
    [InlineKeyboardButton(text='Обучение', web_app=WebAppInfo(url="https://academywebapp-kriswis.amvera.io/"))],
    [InlineKeyboardButton(text='❓ FAQ', callback_data='start|faq'), 
    InlineKeyboardButton(text='👨‍💻 Поддержка', callback_data='start|support')]])

    if (user_status == const.supportAgent):
        kb.inline_keyboard.append([InlineKeyboardButton(text='📨 Активные тикеты', callback_data='start|supportTickets')])

    if (user_status == const.leader):
        kb.inline_keyboard.append([InlineKeyboardButton(text='📊 Статистика', callback_data='start|stats')])

    return kb


# Клавиатура меню отмены операции
def cancel_operation():
    kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Меню', callback_data='start_menu')]])

    return kb


# Клавиатура с возвратом в главное меню
def backTo_mainMenu_kb():
    kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='↩️ Назад', callback_data='start_menu')]])

    return kb