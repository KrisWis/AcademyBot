from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.models import SupportTicketsOrm
import math

# Клавиатура со всеми тикетами поддержки на данный момент
def supportTickets_kb(supportTickets: list[SupportTicketsOrm], current_page_index: int = 0):
    inline_keyboard = []

    tickets_per_page = 10

    buttons = [[InlineKeyboardButton(text=f"@{supportTicket.user.username}", callback_data=f'supportTickets|{supportTicket.id}')] for supportTicket in supportTickets]

    pages_amount = math.ceil(len(supportTickets) / tickets_per_page)

    pages = [buttons[i:i + tickets_per_page] for i in range(0, len(buttons), tickets_per_page)]

    for _, page in enumerate(pages[current_page_index], start=1):
        for button in page:
            inline_keyboard.append([button])

    action_kb_buttons = []

    if current_page_index > 0:
        action_kb_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"supportTickets|page|{current_page_index}|prev"))

    if pages_amount > 1 and current_page_index < pages_amount - 1:
        action_kb_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"supportTickets|page|{current_page_index}|next"))

    inline_keyboard.append(action_kb_buttons)

    inline_keyboard.append([InlineKeyboardButton(text="↩️ Назад", callback_data="start_menu")])

    kb = InlineKeyboardMarkup(
    inline_keyboard=inline_keyboard)

    return kb


# Клавиатура, отсылаемая Агенту поддержки для ответа пользователю
def supportAgent_answer_to_supportTicket_kb(supportTicket_id: int):
    kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='🤙 Ответить', callback_data=f'supportTickets|{supportTicket_id}|answer')]])

    return kb


# Клавиатура, отсылаемая пользователю для ответа Агенту Поддержки
def user_answer_to_supportTicket_kb(supportTicket_id: int):
    kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='🤙 Ответить', callback_data=f'supportTickets|{supportTicket_id}|answer')],
                    [InlineKeyboardButton(text='🔒 Закрыть тикет', callback_data=f'supportTickets|{supportTicket_id}|close')]])

    return kb


# Клавиатура, отсылаемая пользователю для оценивания Агента Поддержки по 5-бальной шкале
def evaluate_supportAgent_kb(supportTicket_id: int):
    kb = InlineKeyboardMarkup(
    inline_keyboard=[[
    InlineKeyboardButton(text='1 🤢', callback_data=f'supportTickets|{supportTicket_id}|evaluate|1'),
    InlineKeyboardButton(text='2 🙁', callback_data=f'supportTickets|{supportTicket_id}|evaluate|2'),
    InlineKeyboardButton(text='3 🙂', callback_data=f'supportTickets|{supportTicket_id}|evaluate|3'),
    InlineKeyboardButton(text='4 😁', callback_data=f'supportTickets|{supportTicket_id}|evaluate|4'),
    InlineKeyboardButton(text='5 🥰', callback_data=f'supportTickets|{supportTicket_id}|evaluate|5')]])

    return kb