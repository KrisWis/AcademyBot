from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from utils.const import statuses
from database.models import UsersRefsOrm
import math

# Клавиатура с меню профиля
def profile_menu():
    kb = InlineKeyboardMarkup(row_width=1, 
    inline_keyboard=[
    [InlineKeyboardButton(text='📥 Пополнить', callback_data='profile|replenish'), 
    InlineKeyboardButton(text='📤 Вывести', callback_data='profile|withdraw')],
    [InlineKeyboardButton(text='🫂 Рефералы', callback_data='profile|referals')],
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
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите нужную вам сумму")

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
def profile_referals_menu(user_status: str):

    if (user_status == statuses["manager"]):
        kb = InlineKeyboardMarkup(
        inline_keyboard=[
        [InlineKeyboardButton(text='📊 Статистика', callback_data='profile_referals_menu|dynamics'),
        InlineKeyboardButton(text='📁 Материалы', callback_data='profile_referals_menu|materials')],
        [InlineKeyboardButton(text='👥 Ваши рефералы', callback_data='profile_referals_menu|referals')],
        [InlineKeyboardButton(text='↩️ Назад', callback_data='start|profile')]])
    else:
        kb = InlineKeyboardMarkup(
        inline_keyboard=[
        [InlineKeyboardButton(text='📊 Статистика', callback_data='profile_referals_menu|dynamics'),
        InlineKeyboardButton(text='📁 Материалы', callback_data='profile_referals_menu|materials')],
        [InlineKeyboardButton(text='↩️ Назад', callback_data='start|profile')]])

    return kb


# Клавиатура с возвратом назад в меню "Рефералы"
def profile_referals_back_kb():
    kb = InlineKeyboardMarkup(row_width=1, 
    inline_keyboard=[
    [InlineKeyboardButton(text='↩️ Назад', callback_data='profile|referals')]])

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


# Клавиатура с чеком на вывод по кнопке "Пополнить"
def send_check_url_kb(check_url: str):
    kb = InlineKeyboardMarkup(row_width=1, 
    inline_keyboard=[
    [InlineKeyboardButton(text='Вывести 📤', url=check_url)]])

    return kb


# Клавиатура со всеми рефералами менеджера на данный момент
def manager_referals_kb(manager_referals: list[UsersRefsOrm], current_page_index: int = 0):
    inline_keyboard = []

    referals_per_page = 10

    buttons = [[InlineKeyboardButton(text=f"@{manager_referal.user.username}", callback_data=f'manager_referals|{manager_referal.user_id}')] for manager_referal in manager_referals]

    pages_amount = math.ceil(len(manager_referals) / referals_per_page)

    pages = [buttons[i:i + referals_per_page] for i in range(0, len(buttons), referals_per_page)]

    for _, page in enumerate(pages[current_page_index], start=1):
        for button in page:
            inline_keyboard.append([button])

    action_kb_buttons = []

    if current_page_index > 0:
        action_kb_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"'manager_referals|page|{current_page_index}|prev"))

    if pages_amount > 1 and current_page_index < pages_amount - 1:
        action_kb_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"'manager_referals|page|{current_page_index}|next"))

    inline_keyboard.append(action_kb_buttons)

    inline_keyboard.append([InlineKeyboardButton(text="↩️ Назад", callback_data="profile|referals")])

    kb = InlineKeyboardMarkup(
    inline_keyboard=inline_keyboard)

    return kb


# Клавиатура для изменения реферального процента реферала менеджера
def manager_referal_profile_kb():
    kb = InlineKeyboardMarkup( 
    inline_keyboard=[
    [InlineKeyboardButton(text='✍️ Изменить процент', 
    callback_data='manager_referal|change_percent')]])

    return kb
