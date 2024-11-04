from aiogram import types
from InstanceBot import router, bot
from utils import text
from keyboards import Keyboards

async def send_support(call: types.CallbackQuery) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    await call.message.answer(text.support_text, reply_markup=Keyboards.backTo_mainMenu_kb())
    

def hand_add():
    router.callback_query.register(send_support, lambda c: c.data == 'start|support')
