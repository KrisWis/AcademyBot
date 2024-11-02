from aiogram import types, Dispatcher
from utils import text
from InstanceBot import router
from aiogram.filters import CommandStart, Command, StateFilter

async def start(message: types.Message):
    await message.answer(text.start_text)


def hand_add(dp: Dispatcher):
    router.message.register(start, StateFilter(None), CommandStart())
