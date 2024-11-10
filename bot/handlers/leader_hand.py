from aiogram import types
from InstanceBot import router, bot
from utils import leader_text
from keyboards import leaderKeyboards
from database.orm import AsyncORM
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from utils import const
from states.Leader import LeaderMenuStates


# Отправка меню руководителя при вводе "/leader"
async def leader_menu(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    user_status = await AsyncORM.get_user_status(user_id)

    if user_status in [const.leader, const.developer]:
        await message.answer(leader_text.leader_menu_text, 
        reply_markup=leaderKeyboards.leader_menu_kb())

        await state.set_state(None)


# Отправка меню руководителя при с помощью инлайн кнопки
async def call_leader_menu(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    user_status = await AsyncORM.get_user_status(user_id)

    if user_status in [const.leader, const.developer]:
        await call.message.answer(leader_text.leader_menu_text, 
        reply_markup=leaderKeyboards.leader_menu_kb())

        await state.set_state(None)


# Отправка сообщения со статистикой
async def send_stats_selection(call: types.CallbackQuery):
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    await call.message.answer(
        text=leader_text.stats_title_text,
        reply_markup=leaderKeyboards.stats_kb()
    )


# Обработка клавиатуры со статистикой
async def send_stats(call: types.CallbackQuery):
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    temp = call.data.split('|')

    all_users = await AsyncORM.get_users(period=temp[1])

    geo = await AsyncORM.get_users(period=temp[1], geo=True)

    temp_dict = {
        "day": "день",
        "week": "неделю",
        "month": "месяц",
        "all": "все время",
    }

    purchased_courses = await AsyncORM.get_purchased_courses(period=temp[1])

    replenishBalances_info = await AsyncORM.get_replenishBalances_sum(period=temp[1])

    withdrawBalances_info = await AsyncORM.get_withdrawBalances_sum(period=temp[1])

    await call.message.answer(
        text=leader_text.stats_text.format(temp_dict[temp[1]], len(all_users), geo, 
                                        len(purchased_courses), replenishBalances_info, withdrawBalances_info),
        reply_markup=leaderKeyboards.stats_kb()
    )


# Отправка сообщения для отправки id тикета поддержки
async def wait_supportTicket_id(call: types.CallbackQuery, state: FSMContext) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    await call.message.answer(
        text=leader_text.send_supportTicketID_text,
    )

    await state.set_state(LeaderMenuStates.write_supportTicket_id)


# Отправка сообщений тикета поддержки
async def send_messages_of_supportTicket(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    message_id = message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id - 1)

    supportTicket_id = int(message.text)

    supportTicket = await AsyncORM.get_supportTicket(supportTicket_id)

    if supportTicket:
        if supportTicket.status != "open":
            await message.answer(
                text=leader_text.send_messages_of_supportTicket_text.format(supportTicket_id),
            )

            await message.answer(leader_text.sending_supportTicket_user_start_message_text.format(supportTicket.user.username, supportTicket.text))

            previous_message_from = "user"

            for message_text in supportTicket.messages:
                if message_text:
                    if previous_message_from == "user":
                        await message.answer(leader_text.sending_supportTicket_supportAgent_message_text.format(supportTicket.supportAgent.username, message_text))
                        previous_message_from = "supportAgent"
                    
                    elif previous_message_from == "supportAgent":
                        await message.answer(leader_text.sending_supportTicket_user_message_text.format(supportTicket.user.username, message_text))
                        previous_message_from = "user"

            await state.set_state(None)

            return


    await message.answer(
        text=leader_text.send_supportTicketID_error_text,
    )
    

def hand_add():
    router.message.register(leader_menu, StateFilter("*"), Command("leader_menu"))

    router.message.register(send_messages_of_supportTicket, StateFilter(LeaderMenuStates.write_supportTicket_id))

    router.callback_query.register(call_leader_menu, lambda c: c.data == 'leader_menu')

    router.callback_query.register(send_stats_selection, lambda c: c.data == 'leader_menu|stats')

    router.callback_query.register(wait_supportTicket_id, lambda c: c.data == 'leader_menu|supportTicket')

    router.callback_query.register(send_stats, lambda c: c.data.startswith('stats'))