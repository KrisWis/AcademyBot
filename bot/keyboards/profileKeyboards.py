from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

# Клавиатура с меню профиля
def profile_menu():
    kb = InlineKeyboardMarkup(row_width=1, 
    inline_keyboard=[
    [InlineKeyboardButton(text='📥 Пополнить', callback_data='profile|replenish'), 
    InlineKeyboardButton(text='📤 Вывести', callback_data='profile|withdraw')],
    [InlineKeyboardButton(text='🫂 Рефералы', callback_data='profile|referrals')],
    [InlineKeyboardButton(text='🗂 Пользовательское соглашение', url="https://ru.lipsum.com/")],
    [InlineKeyboardButton(text='↩️ Назад', callback_data='start_menu')]])

    return kb


# Клавиатура с выбором суммы
def profile_choose_sum_kb():
    kb = [
        [KeyboardButton(text="5000 RUB")],
        [KeyboardButton(text="10000 RUB")],
        [KeyboardButton(text="↩️ Назад")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите нужную вам сумму", one_time_keyboard=True)

    return keyboard


# Клавиатура с подтверждением/отменой
def profile_confirmation_menu():
    kb = InlineKeyboardMarkup(row_width=1, 
    inline_keyboard=[
    [InlineKeyboardButton(text='✅ Подтвердить', callback_data='profile_confirmation|agree')],
    [InlineKeyboardButton(text='❌ Отменить', callback_data='cancel_operation')]])

    return kb


# Клавиатура с меню выбора способа оплаты для пополнения
def profile_choose_payment_menu():
    kb = InlineKeyboardMarkup(row_width=1, 
    inline_keyboard=[
    [InlineKeyboardButton(text='🤖 CryptoBot', callback_data='profile_choose_replenish|CryptoBot')],
    [InlineKeyboardButton(text='🇷🇺 Банковская карта', callback_data='profile_choose_replenish|bankCard')],
    [InlineKeyboardButton(text='↩️ Назад', callback_data='start|profile')]])

    return kb


# Клавиатура с меню выбора способа оплаты для вывода
def profile_choose_withdraw_menu():
    kb = InlineKeyboardMarkup(row_width=1, 
    inline_keyboard=[
    [InlineKeyboardButton(text='🤖 CryptoBot', callback_data='profile_choose_withdraw|CryptoBot')],
    [InlineKeyboardButton(text='🇷🇺 Банковская карта', callback_data='profile_choose_withdraw|bankCard')],
    [InlineKeyboardButton(text='↩️ Назад', callback_data='start|profile')]])

    return kb


# Клавиатура с меню "Рефералы"
def profile_referrals_menu():
    kb = InlineKeyboardMarkup(row_width=1, 
    inline_keyboard=[
    [InlineKeyboardButton(text='📊 Статистика', callback_data='profile_referrals_menu|dynamics'),
    InlineKeyboardButton(text='📁 Материалы', callback_data='profile_referrals_menu|materials')],
    [InlineKeyboardButton(text='↩️ Назад', callback_data='start|profile')]])

    return kb


# Клавиатура с возвратом назад в меню "Рефералы"
def profile_referrals_back_kb():
    kb = InlineKeyboardMarkup(row_width=1, 
    inline_keyboard=[
    [InlineKeyboardButton(text='↩️ Назад', callback_data='profile|referrals')]])

    return kb


# Клавиатура для проверки оплаты с помощью криптовалюты
def check_payment_crypto(pay_url, invoice_id):
    kb = InlineKeyboardMarkup(row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text='Оплатить', url=pay_url)],
        [InlineKeyboardButton(text='Проверить оплату', callback_data=f'payment|CryptoBot|{invoice_id}')],
        [InlineKeyboardButton(text='Отменить', callback_data=f'payment|CryptoBot|back')]
        ])

    return kb