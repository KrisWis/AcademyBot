from aiogram import types
from InstanceBot import router, bot
from utils import leader_text
from keyboards import leaderKeyboards
from database.orm import AsyncORM


# Отправка сообщения со статистикой
async def send_stats_selection(call: types.CallbackQuery) -> None:
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
    

def hand_add():
    router.callback_query.register(send_stats_selection, lambda c: c.data == 'start|stats')

    router.callback_query.register(send_stats, lambda c: c.data.startswith('stats'))