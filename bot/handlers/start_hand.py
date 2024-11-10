from aiogram import types
from utils import text
from InstanceBot import router, bot
from aiogram.filters import CommandStart, StateFilter
import datetime
from database.orm import AsyncORM
from aiogram.fsm.context import FSMContext
from filters import Sub
from keyboards import globalKeyboards


# Отправка стартового меню при вводе "/start"
async def start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    now = datetime.datetime.now()

    data = await state.get_data()

    date_format = "%Y-%m-%d %H:%M:%S"

    formatted_time = now.strftime(date_format)

    formatted_time = datetime.datetime.strptime(formatted_time, date_format)
    
    if not await AsyncORM.get_user(user_id):
        referrer_id = message.text[7:] or None

        if "referrer_id" in data:
            referrer_id = data["referrer_id"]

        if referrer_id:
            if referrer_id.isdigit() and referrer_id != str(user_id):

                await bot.send_message(
                    chat_id=referrer_id,
                    text=text.new_referral_text.format(username)
                )

                referrer_id = int(referrer_id)  

        await AsyncORM.add_user(
            user_id,
            username,
            formatted_time,
            message.from_user.language_code,
            referrer_id
        )
    
    user_status = await AsyncORM.get_user_status(user_id)
    await message.answer_animation(caption=text.start_text, 
    reply_markup=globalKeyboards.start_menu(user_status), 
    animation='https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif')

    await state.set_state(None)


def hand_add():
    router.message.register(start, StateFilter("*"), Sub(), CommandStart())
