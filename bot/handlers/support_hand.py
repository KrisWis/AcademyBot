from aiogram import types
from InstanceBot import router, bot, dp
from utils import support_text
from keyboards import globalKeyboards
from states.Student import SupportStates
from aiogram.fsm.context import FSMContext, StorageKey
from aiogram.filters import StateFilter
from database.orm import AsyncORM
from keyboards import supportKeyboards
import re
import math
from states.SupportAgent import SupportAgentStates
from RunBot import logger
from states.Student import SupportStates

# Отправка сообщения, чтобы пользователь отправил сообщение в поддержку
async def send_support(call: types.CallbackQuery, state: FSMContext) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    await call.message.answer(support_text.support_text, reply_markup=globalKeyboards.backTo_mainMenu_kb())

    await state.set_state(SupportStates.write_text_of_supportTicket)
    

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
async def send_supportTickets(call: types.CallbackQuery) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    supportTickets = await AsyncORM.get_all_opened_supportTickets()

    tickets_per_page = 10

    pages_amount = math.ceil(len(supportTickets) / tickets_per_page)

    if len(supportTickets) > 0:
        await call.message.answer(support_text.send_supportTickets_text.format(1, pages_amount), 
                                reply_markup=supportKeyboards.supportTickets_kb(supportTickets))
    else:
        await call.message.answer(support_text.supportTickets_none_text)


# Обработка перелистывания страниц в инлайн клавиатуре тикетов поддержки
async def send_supportTickets_page(call: types.CallbackQuery) -> None:
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

    supportTickets = await AsyncORM.get_all_opened_supportTickets()

    tickets_per_page = 10

    pages_amount = math.ceil(len(supportTickets) / tickets_per_page)

    await call.message.answer(support_text.send_supportTickets_text.format(page + 1, pages_amount), 
                            reply_markup=supportKeyboards.supportTickets_kb(supportTickets, page))


# Отправка тикета поддержки пользователя
async def send_supportTicket(call: types.CallbackQuery) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    temp = call.data.split("|")

    supportTicket_id = int(temp[1])

    supportTicket = await AsyncORM.get_supportTicket(supportTicket_id)

    await AsyncORM.add_supportAgent_for_supportTicket(supportTicket_id, user_id)

    await call.message.answer(support_text.send_supportTicket_text.
    format(supportTicket.id, supportTicket.user.username, supportTicket.text),
    reply_markup=supportKeyboards.supportAgent_answer_to_supportTicket_kb(supportTicket_id))


# Отправка сообщение для того, чтобы агент поддержки начал писать ответ на тикет поддержки
async def answer_to_supportTicket(call: types.CallbackQuery, state: FSMContext) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    temp = call.data.split("|")

    supportTicket_id = int(temp[1])

    supportTicket = await AsyncORM.get_supportTicket(supportTicket_id)

    await state.update_data(answer_supportTicket_id=supportTicket_id)

    await call.message.answer(support_text.answer_to_supportTicket_text)

    if supportTicket.user_id == user_id:
        await state.set_state(SupportStates.write_text_for_answer_supportTicket)

    elif supportTicket.supportAgent_id == user_id:
        await state.set_state(SupportAgentStates.write_text_for_answer)


# Отправка ответа агента поддержки пользователю
async def send_supportAgent_answer_for_supportTicket(message: types.Message, state: FSMContext) -> None:
    username = message.from_user.username

    data = await state.get_data()

    supportAgent_answer_text = message.text

    supportTicket_id = data["answer_supportTicket_id"]

    supportTicket = await AsyncORM.get_supportTicket(supportTicket_id)

    if (supportTicket.status != "active"):
        try:
            await AsyncORM.change_supportTicket_status(supportTicket_id, "active")

            await bot.send_message(chat_id=supportTicket.user_id, 
                    text=support_text.supportAgent_answer_supportTicket_text.format(username, supportTicket_id, supportAgent_answer_text), 
                    reply_markup=supportKeyboards.user_answer_to_supportTicket_kb(supportTicket_id))
            
            await message.answer(support_text.send_answer_for_supportTicket_success_text)

        except Exception as e:
            logger.info(f"Ошибка при ответе на тикет поддержки: {e}")
            await message.answer(support_text.send_answer_for_supportTicket_error_text)

    else:
        await message.answer(support_text.send_answer_for_supportTicket_alreadyAnswered_text)

    await state.clear()


# Отправка ответа пользователя агенту поддержки
async def send_user_answer_for_supportTicket(message: types.Message, state: FSMContext) -> None:
    username = message.from_user.username

    data = await state.get_data()

    supportAgent_answer_text = message.text

    supportTicket_id = data["answer_supportTicket_id"]

    supportTicket = await AsyncORM.get_supportTicket(supportTicket_id)

    try:
        await bot.send_message(chat_id=supportTicket.supportAgent_id, 
                text=support_text.user_answer_supportTicket_text.format(username, supportTicket_id, supportAgent_answer_text), 
                reply_markup=supportKeyboards.supportAgent_answer_to_supportTicket_kb(supportTicket_id))
        
        await message.answer(support_text.send_answer_for_supportTicket_success_text)

    except Exception as e:
        logger.info(f"Ошибка при ответе на тикет поддержки: {e}")
        await message.answer(support_text.send_answer_for_supportTicket_error_text)

    await state.clear()


# Закрытие тикета поддержки пользователем
async def close_supportTicket(call: types.CallbackQuery, state: FSMContext) -> None:
    user_id = call.from_user.id
    username = call.from_user.username
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    temp = call.data.split("|")

    supportTicket_id = int(temp[1])

    supportTicket = await AsyncORM.get_supportTicket(supportTicket_id)

    await AsyncORM.change_supportTicket_status(supportTicket_id, "closed")

    await bot.send_message(chat_id=supportTicket.supportAgent_id, 
        text=support_text.user_answer_supportTicket_text.format(username, supportTicket_id))
    
    # TODO: проверить прошлый функционал, доделать здесь - добавить возможность оценить сотрудника (добавить модель для агента поддержки), и сделать добавление сообщений тикета в бд



def hand_add():
    router.message.register(append_supportTicket_success, StateFilter(SupportStates.write_text_of_supportTicket))

    router.message.register(send_supportAgent_answer_for_supportTicket, StateFilter(SupportAgentStates.write_text_for_answer))

    router.message.register(send_user_answer_for_supportTicket, StateFilter(SupportStates.write_text_for_answer_supportTicket))

    router.callback_query.register(send_support, lambda c: c.data == 'start|support')

    router.callback_query.register(send_supportTickets, lambda c: c.data == 'start|supportTickets')

    router.callback_query.register(send_supportTickets_page, lambda c: c.data.startswith('supportTickets|page'))

    router.callback_query.register(send_supportTicket, lambda c: re.match(r"^supportTickets\|(\w+)$", c.data))

    router.callback_query.register(answer_to_supportTicket, lambda c: re.match(r"^supportTickets\|([^\|]+)\|answer$", c.data))

    router.callback_query.register(close_supportTicket, lambda c: re.match(r"^supportTickets\|([^\|]+)\|close$", c.data))