from aiogram import types
from InstanceBot import router, bot
from utils import support_text
from keyboards import Keyboards
from states import User
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from database.orm import AsyncORM

# Отправка сообщения, чтобы пользователь отправил сообщение
async def send_support(call: types.CallbackQuery, state: FSMContext) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    await call.message.answer(support_text.support_text, reply_markup=Keyboards.backTo_mainMenu_kb())

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


def hand_add():
    router.message.register(append_supportTicket_success, StateFilter(User.SupportStates.write_text_of_supportTicket))

    router.callback_query.register(send_support, lambda c: c.data == 'start|support')
