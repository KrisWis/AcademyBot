from aiogram import types
from utils import text
from InstanceBot import router
from aiogram.filters import CommandStart, StateFilter
import datetime
from database.orm import AsyncORM
from aiogram.fsm.context import FSMContext
from filters import Sub
from keyboards import Keyboards

async def start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    now = datetime.datetime.now()

    # await AsyncORM.create_tables()

    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    if not await AsyncORM.user_exists(user_id):
        start_tag = message.text[7:]

        if len(start_tag) != 0:
            if start_tag.isdigit() and start_tag != str(user_id):
                start_tag = start_tag
        else:
            start_tag = 'Органика'

        await AsyncORM.add_user(
            user_id,
            username,
            formatted_time,
            message.from_user.language_code,
            start_tag,
            "Ученик",
            [],
            0
        )
    
    await message.answer_animation(caption=text.start_text, reply_markup=Keyboards.start_menu(), 
    animation='https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif')

    await state.set_state(None)


def hand_add():
    router.message.register(start, StateFilter("*"), Sub(), CommandStart())
