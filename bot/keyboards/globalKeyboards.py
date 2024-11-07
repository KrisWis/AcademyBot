from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

# Клавиатура стартового меню
def start_menu(isSupportAgent: bool = False):
    kb = InlineKeyboardMarkup(row_width=1, 
    inline_keyboard=[
    [InlineKeyboardButton(text='🎓 Профиль', callback_data='start|profile')],
    [InlineKeyboardButton(text='Обучение', web_app=WebAppInfo(url="https://academywebapp-kriswis.amvera.io/"))],
    [InlineKeyboardButton(text='❓ FAQ', callback_data='start|faq'), 
    InlineKeyboardButton(text='👨‍💻 Поддержка', callback_data='start|support')]])

    if (isSupportAgent):
        kb.inline_keyboard.append([InlineKeyboardButton(text='📨 Активные тикеты', callback_data='start|supportTickets')])

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