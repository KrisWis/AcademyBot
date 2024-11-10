from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Клавиатура для меню руководителя
def leader_menu_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='📊 Статистика', callback_data='leader_menu|stats')],
        [InlineKeyboardButton(text='👨‍💻 Просмотреть тикет', callback_data='leader_menu|supportTicket')],
        [InlineKeyboardButton(text='💲 Изменить баланс', callback_data='leader_menu|changeBalance')],
        [InlineKeyboardButton(text='👤 Изменить статус', callback_data='leader_menu|changeStatus')]])
    
    return kb


# Клавиатура для статистики
def stats_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='День', callback_data='stats|day'),
        InlineKeyboardButton(text='Неделя', callback_data='stats|week'),
        InlineKeyboardButton(text='Месяц', callback_data='stats|month'),
        InlineKeyboardButton(text='Все время', callback_data='stats|all')],
        [InlineKeyboardButton(text='Вернуться в меню', callback_data='leader_menu')]])
    
    return kb


# Клавиатура для выбора нового статуса пользователя
def change_user_status_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='👤 Ученик', callback_data='changeStatus|student')],
        [InlineKeyboardButton(text='🕴 Агент поддержки', callback_data='changeStatus|supportAgent')],
        [InlineKeyboardButton(text='👨‍🏫 Менеджер', callback_data='changeStatus|manager')],
        [InlineKeyboardButton(text='🤵‍♂️ Партнёр', callback_data='changeStatus|partner')],
        [InlineKeyboardButton(text='👨‍💻 Разработчик', callback_data='changeStatus|developer')],
        [InlineKeyboardButton(text='🤴 Руководитель', callback_data='changeStatus|leader')]])
    
    return kb