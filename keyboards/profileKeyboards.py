from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

# Меню профиля
def profile_menu():
    kb = InlineKeyboardMarkup(row_width=1, 
    inline_keyboard=[
    [InlineKeyboardButton(text='📥 Пополнить', callback_data='profile|replenish'), 
    InlineKeyboardButton(text='📤 Вывести', callback_data='profile|withdraw')],
    [InlineKeyboardButton(text='🫂 Рефералы', callback_data='profile|referrals')],
    [InlineKeyboardButton(text='🗂 Пользовательское соглашение', url="https://ru.lipsum.com/")],
    [InlineKeyboardButton(text='↩️ Назад', callback_data='start_menu')]])

    return kb


def profile_choose_sum_kb():
    kb = [
        [KeyboardButton(text="5000 RUB")],
        [KeyboardButton(text="10000 RUB")],
        [KeyboardButton(text="↩️ Назад")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите нужную вам сумму", one_time_keyboard=True)

    return keyboard

def profile_confirmation_menu():
    kb = InlineKeyboardMarkup(row_width=1, 
    inline_keyboard=[
    [InlineKeyboardButton(text='✅ Подтвердить', callback_data='profile_confirmation|agree')],
    [InlineKeyboardButton(text='❌ Отменить', callback_data='cancel_operation')]])

    return kb

# Кнопка "📥 Пополнить"
def profile_choose_payment_menu():
    kb = InlineKeyboardMarkup(row_width=1, 
    inline_keyboard=[
    [InlineKeyboardButton(text='🤖 CryptoBot', callback_data='profile_choose_payment|CryptoBot')],
    [InlineKeyboardButton(text='🇷🇺 Банковская карта', callback_data='profile_choose_payment|bankCard')],
    [InlineKeyboardButton(text='↩️ Назад', callback_data='start|profile')]])

    return kb

# Кнопка "📤 Вывести"
def profile_choose_withdraw_menu():
    kb = InlineKeyboardMarkup(row_width=1, 
    inline_keyboard=[
    [InlineKeyboardButton(text='🤖 CryptoBot', callback_data='profile_choose_withdraw|CryptoBot')],
    [InlineKeyboardButton(text='🇷🇺 Банковская карта', callback_data='profile_choose_withdraw|bankCard')],
    [InlineKeyboardButton(text='↩️ Назад', callback_data='start|profile')]])

    return kb

# Кнопка "🫂 Рефералы"
def profile_referrals_menu():
    kb = InlineKeyboardMarkup(row_width=1, 
    inline_keyboard=[
    [InlineKeyboardButton(text='📊 Статистика', callback_data='profile_referrals_menu|dynamics'),
    InlineKeyboardButton(text='📁 Материалы', callback_data='profile_referrals_menu|materials')],
    [InlineKeyboardButton(text='↩️ Назад', callback_data='start|profile')]])

    return kb

def profile_referrals_back_kb():
    kb = InlineKeyboardMarkup(row_width=1, 
    inline_keyboard=[
    [InlineKeyboardButton(text='↩️ Назад', callback_data='profile|referrals')]])

    return kb