from aiogram import types
from InstanceBot import router
from InstanceBot import bot
from aiogram.fsm.context import FSMContext
from utils import text
from keyboards import Keyboards

async def start_menu(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    await call.message.answer_animation(caption=text.start_text, 
    reply_markup=Keyboards.start_menu(), 
    animation='https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif')

    await state.set_state(None)

def hand_add():
    router.callback_query.register(start_menu, lambda c: c.data == 'profile|back')
