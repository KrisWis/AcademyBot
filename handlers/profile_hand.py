from aiogram import types
from utils import profile_text
from InstanceBot import router
from utils import text
from database.orm import AsyncORM
from InstanceBot import bot
from keyboards import profileKeyboards
from states import ProfileStates
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from credit_card_checker import CreditCardChecker

async def send_profile(call: types.CallbackQuery) -> None:
    user_id = call.from_user.id
    profile_info = await AsyncORM.get_profile_info(user_id)
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    await call.message.answer(profile_text.profile_text.
    format(profile_info.status, profile_info.user.user_reg_time, 
    len(profile_info.completed_courses), ";\n".join(profile_info.completed_courses), profile_info.balance), 
    reply_markup=profileKeyboards.profile_menu())
    

# "Пополнить"
async def send_profile_choose_payment(call: types.CallbackQuery, state: FSMContext) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    kb_messageid = await call.message.answer(profile_text.profile_choose_payment_text, 
    reply_markup=profileKeyboards.profile_choose_payment_menu())

    await state.update_data(kb_messageid=kb_messageid.message_id)


async def send_profile_choose_sumOfPayment(call: types.CallbackQuery, state: FSMContext) -> None:
    user_id = call.from_user.id

    data = await state.get_data()

    await bot.delete_message(chat_id=user_id, message_id=data["kb_messageid"])

    await call.message.answer(profile_text.profile_choose_sumOfPayment_text, reply_markup=profileKeyboards.profile_choose_sum_kb())

    await state.set_state(ProfileStates.choose_sumOfPayment)


async def send_profile_made_payment(message: types.Message):
    user_id = message.from_user.id
    message_id = message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id - 1)

    if message.text == "↩️ Назад":
        await message.answer(profile_text.profile_choose_sumOfPayment_text, 
        reply_markup=profileKeyboards.profile_choose_payment_menu())


# "Вывести"
async def send_profile_choose_withdraw(call: types.CallbackQuery, state: FSMContext) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    kb_messageid = await call.message.answer(profile_text.profile_choose_withdraw_text, 
    reply_markup=profileKeyboards.profile_choose_withdraw_menu())

    await state.update_data(kb_messageid=kb_messageid.message_id)


async def send_profile_choose_sumOfWithdraw(call: types.CallbackQuery, state: FSMContext) -> None:
    user_id = call.from_user.id
    temp = call.data.split("|")

    data = await state.get_data()

    await bot.delete_message(chat_id=user_id, message_id=data["kb_messageid"])

    await call.message.answer(profile_text.profile_choose_sumOfWithdraw_text, reply_markup=profileKeyboards.profile_choose_sum_kb())
    
    await state.set_state(ProfileStates.choose_sumOfWithdraw)
    
    if temp[1] == "bankCard":
        await state.update_data(methodOfWithdraw="Банковская карта")

    elif temp[1] == "CryptoBot":
        await state.update_data(methodOfWithdraw="Криптовалюта")


async def send_profile_write_cardNumber(message: types.Message, state: FSMContext) -> None:

    if message.text == "↩️ Назад":
        kb_messageid = await message.answer(profile_text.profile_choose_withdraw_text, 
        reply_markup=profileKeyboards.profile_choose_withdraw_menu())

        await state.update_data(kb_messageid=kb_messageid.message_id)

        await state.set_state(None)

        return

    sumofWithdraw = message.text

    data = await state.get_data()
    
    await state.update_data(sumOfWithdraw=sumofWithdraw)

    if data["methodOfWithdraw"] == "Банковская карта":

        await message.answer(profile_text.profile_write_cardNumber_text)

        await state.set_state(ProfileStates.write_cardNumber)

    elif data["methodOfWithdraw"] == "Криптовалюта":

        await message.answer(profile_text.profile_confirmation_text
        .format(data["methodOfWithdraw"], "Криптовалюта", sumofWithdraw), reply_markup=profileKeyboards.profile_confirmation_menu())

        await state.set_state(None)

async def send_profile_confirmation(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()

    cart_details = message.text

    if CreditCardChecker(cart_details).valid():
        await message.answer(profile_text.profile_confirmation_text
        .format(data["methodOfWithdraw"], cart_details, data["sumOfWithdraw"]), reply_markup=profileKeyboards.profile_confirmation_menu())

        await state.set_state(None)
    else: 
        await message.answer(text.invalid_data_text)


async def send_withdraw_agree(call: types.CallbackQuery, state: FSMContext) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    await call.message.answer(profile_text.profile_withDraw_agree)

    await state.set_state(None)


def hand_add():
    router.message.register(send_profile_made_payment, StateFilter(ProfileStates.choose_sumOfPayment))

    router.message.register(send_profile_write_cardNumber, StateFilter(ProfileStates.choose_sumOfWithdraw))

    router.message.register(send_profile_confirmation, StateFilter(ProfileStates.write_cardNumber))

    router.callback_query.register(send_profile, lambda c: c.data in ['start|profile', "profile_choose_payment|back", "profile_choose_withdraw|back"])

    router.callback_query.register(send_profile_choose_payment, lambda c: c.data == 'profile|replenish')

    router.callback_query.register(send_profile_choose_sumOfPayment, lambda c: c.data in ["profile_choose_payment|CryptoBot", "profile_choose_payment|bankCard"])

    router.callback_query.register(send_profile_choose_withdraw, lambda c: c.data == 'profile|withdraw')

    router.callback_query.register(send_profile_choose_sumOfWithdraw, lambda c: c.data in ["profile_choose_withdraw|CryptoBot", "profile_choose_withdraw|bankCard"])

    router.callback_query.register(send_withdraw_agree, lambda c: c.data == "profile_confirmation|agree")
