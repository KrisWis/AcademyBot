from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.models import SupportTicketsOrm
import math

# Клавиатура со всеми тикетами поддержки на данный момент
def support_tickets_kb(support_tickets: list[SupportTicketsOrm], current_page_index: int = 0):
    inline_keyboard = []

    tickets_per_page = 10

    buttons = [[InlineKeyboardButton(text=f"@{support_ticket.user.username}", callback_data=f'support_tickets|{support_ticket.id}')] for support_ticket in support_tickets]

    pages_amount = math.ceil(len(support_tickets) / tickets_per_page)

    pages = [buttons[i:i + tickets_per_page] for i in range(0, len(buttons), tickets_per_page)]

    for _, page in enumerate(pages[current_page_index], start=1):
        for button in page:
            inline_keyboard.append([button])

    action_kb_buttons = []

    if current_page_index > 0:
        action_kb_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"support_tickets|page|{current_page_index}|prev"))

    if pages_amount > 1 and current_page_index < pages_amount - 1:
        action_kb_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"support_tickets|page|{current_page_index}|next"))

    inline_keyboard.append(action_kb_buttons)

    kb = InlineKeyboardMarkup(
    inline_keyboard=inline_keyboard)

    return kb