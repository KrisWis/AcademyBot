from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Клавиатура для меню рукводителя
def leader_menu_kb():
    kb = InlineKeyboardMarkup(row_width=4, inline_keyboard=[
        [InlineKeyboardButton(text='📊 Статистика', callback_data='leader_menu|stats')],
        [InlineKeyboardButton(text='👨‍💻 Просмотреть тикет', callback_data='leader_menu|supportTicket')],
        [InlineKeyboardButton(text='💲 Изменить баланс', callback_data='leader_menu|changeBalance')],
        [InlineKeyboardButton(text='👤 Изменить статус', callback_data='leader_menu|changeStatus')]])
    
    return kb


# Клавиатура для статистики
def stats_kb():
    kb = InlineKeyboardMarkup(row_width=4, inline_keyboard=[
        [InlineKeyboardButton(text='День', callback_data='stats|day'),
        InlineKeyboardButton(text='Неделя', callback_data='stats|week'),
        InlineKeyboardButton(text='Месяц', callback_data='stats|month'),
        InlineKeyboardButton(text='Все время', callback_data='stats|all')],
        [InlineKeyboardButton(text='Вернуться в меню', callback_data='leader_menu')]])
    
    return kb