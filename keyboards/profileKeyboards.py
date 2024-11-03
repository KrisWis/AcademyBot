from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def profile_menu():
    kb = InlineKeyboardMarkup(row_width=1, 
    inline_keyboard=[
    [InlineKeyboardButton(text='📥 Пополнить', callback_data='profile|replenish'), 
    InlineKeyboardButton(text='📤 Вывести', callback_data='profile|withdraw')],
    [InlineKeyboardButton(text='🫂 Рефералы', callback_data='profile|referrals')],
    [InlineKeyboardButton(text='🗂 Пользовательское соглашение', callback_data='profile|agreement')],
    [InlineKeyboardButton(text='↩️ Назад', callback_data='profile|back')]])

    return kb

def profile_choose_payment_menu():
    kb = InlineKeyboardMarkup(row_width=1, 
    inline_keyboard=[
    [InlineKeyboardButton(text='🤖 CryptoBot', callback_data='profile_choose_payment|cryptoBot')],
    [InlineKeyboardButton(text='🇷🇺 Банковская карта', callback_data='profile_choose_payment|bankCard')],
    [InlineKeyboardButton(text='↩️ Назад', callback_data='profile_choose_payment|back')]])

    return kb

def profile_choose_sumOfPayment_kb():
    kb = [
        [KeyboardButton(text="5000 RUB")],
        [KeyboardButton(text="10000 RUB")],
        [KeyboardButton(text="↩️ Назад")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите нужную вам сумму", one_time_keyboard=True)

    return keyboard