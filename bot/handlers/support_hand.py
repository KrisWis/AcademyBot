from aiogram import types
from InstanceBot import router, bot
from utils import support_text
from keyboards import globalKeyboards
from states import User
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from database.orm import AsyncORM
from keyboards import supportKeyboards
import math

# Отправка сообщения, чтобы пользователь отправил сообщение в поддержку
async def send_support(call: types.CallbackQuery, state: FSMContext) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    await call.message.answer(support_text.support_text, reply_markup=globalKeyboards.backTo_mainMenu_kb())

    await state.set_state(User.SupportStates.write_text_of_supportTicket)
    

# Функция, которая отвечает на отправленное пользователем сообщение
async def append_supportTicket_success(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    supportTicket_text = message.text

    response = await AsyncORM.add_supportTicket(user_id, supportTicket_text)

    if (response):
        await message.answer(support_text.support_addSupportTicket_success_text)
    else:
        await message.answer(support_text.support_addSupportTicket_error_text)

        await state.set_state(None)


# Отправка инлайн клавиатуры тикетов поддержки
async def send_support_tickets(call: types.CallbackQuery) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    support_tickets = await AsyncORM.get_all_supportTickets()

    tickets_per_page = 10

    pages_amount = math.ceil(len(support_tickets) / tickets_per_page)

    if len(support_tickets) > 0:
        await call.message.answer(support_text.send_support_tickets_text.format(1, pages_amount), 
                                reply_markup=supportKeyboards.support_tickets_kb(support_tickets))
    else:
        await call.message.answer(support_text.support_tickets_none_text)


# Обработка перелистывания страниц в инлайн клавиатуре тикетов поддержки
async def send_support_tickets_page(call: types.CallbackQuery) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    temp = call.data.split("|")

    page = temp[2]

    action = temp[3]

    if action == "next":
        page = int(page) + 1

    elif action == "prev":
        page = int(page) - 1

    support_tickets = await AsyncORM.get_all_supportTickets()

    tickets_per_page = 10

    pages_amount = math.ceil(len(support_tickets) / tickets_per_page)

    await call.message.answer(support_text.send_support_tickets_text.format(page + 1, pages_amount), 
                            reply_markup=supportKeyboards.support_tickets_kb(support_tickets, page))


def hand_add():
    router.message.register(append_supportTicket_success, StateFilter(User.SupportStates.write_text_of_supportTicket))

    router.callback_query.register(send_support, lambda c: c.data == 'start|support')

    router.callback_query.register(send_support_tickets, lambda c: c.data == 'start|support_tickets')

    router.callback_query.register(send_support_tickets_page, lambda c: c.data.startswith('support_tickets|page'))
