from aiogram import types
from utils import text
from InstanceBot import router
from aiogram.filters import CommandStart, StateFilter
import datetime
from database.orm import AsyncORM
from aiogram.fsm.context import FSMContext
from filters import Sub

async def start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    now = datetime.datetime.now()
    
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
            now,
            message.from_user.language_code,
            start_tag
        )

        await message.answer(text.start_text)

    else:
        user_info = await AsyncORM.select_user(user_id)
        await message.answer(text.start_text)

    await state.set_state(None)


def hand_add():
    router.message.register(start, StateFilter(None), Sub(), CommandStart())
