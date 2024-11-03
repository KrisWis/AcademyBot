from aiogram import types
from InstanceBot import router
from utils import callhand_text
from database.orm import AsyncORM
from InstanceBot import bot
from keyboards import profileKeyboards
from states import ProfileStates
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

async def profile(call: types.CallbackQuery) -> None:
    user_id = call.from_user.id
    profile_info = await AsyncORM.get_profile_info(user_id)
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    await call.message.answer(callhand_text.profile_text.
    format(profile_info.status, profile_info.user.user_reg_time, 
    len(profile_info.completed_courses), ";\n".join(profile_info.completed_courses), profile_info.balance), 
    reply_markup=profileKeyboards.profile_menu())
    

async def profile_choose_payment(call: types.CallbackQuery) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    await call.message.answer(callhand_text.profile_choose_payment_text, 
    reply_markup=profileKeyboards.profile_choose_payment_menu())


async def profile_choose_sumOfPayment(call: types.CallbackQuery, state: FSMContext) -> None:

    await call.message.answer(callhand_text.profile_choose_sumOfPayment_text, reply_markup=profileKeyboards.profile_choose_sumOfPayment_kb())

    await state.set_state(ProfileStates.choose_sumOfPayment)


async def profile_made_payment(message: types.Message):
    user_id = message.from_user.id
    message_id = message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id - 1)

    if message.text == "↩️ Назад":
        await message.answer(callhand_text.profile_choose_sumOfPayment_text, 
        reply_markup=profileKeyboards.profile_choose_payment_menu())
    

def hand_add():
    router.message.register(profile_made_payment, StateFilter(ProfileStates.choose_sumOfPayment))

    router.callback_query.register(profile, lambda c: c.data in ['start|profile', "profile_choose_payment|back"] )

    router.callback_query.register(profile_choose_payment, lambda c: c.data == 'profile|replenish')

    router.callback_query.register(profile_choose_sumOfPayment, lambda c: c.data in ["profile_choose_payment|cryptoBot", "profile_choose_payment|bankCard"])