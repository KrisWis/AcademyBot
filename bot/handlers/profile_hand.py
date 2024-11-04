from datetime import datetime
from aiogram import types
from utils import profile_text,  text
from InstanceBot import router, bot
from database.orm import AsyncORM
from keyboards import profileKeyboards
from states import ProfileStates
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from credit_card_checker import CreditCardChecker
from database.models import PurchasedCoursesOrm

# Отправка меню профиля
async def send_profile(call: types.CallbackQuery) -> None:
    user_id = call.from_user.id
    profile_info = await AsyncORM.get_profile_info(user_id)
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    await call.message.answer(profile_text.profile_text.
    format(profile_info.status, profile_info.user.user_reg_date, 
    len(profile_info.completed_courses), ";\n".join(profile_info.completed_courses), profile_info.balance), 
    reply_markup=profileKeyboards.profile_menu())
    

# Кнопка "📥 Пополнить"
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


# Кнопка "📤 Вывести"
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


# Кнопка "🫂 Рефералы"
async def send_referrals_menu(call: types.CallbackQuery, state: FSMContext) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id
    bot_info = await bot.get_me()
    bot_username = bot_info.username

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    await call.message.answer(profile_text.profile_referrals_menu_text.
    format(f'https://t.me/{bot_username}?start={user_id}'), reply_markup=profileKeyboards.profile_referrals_menu())


async def send_referrals_dynamics(call: types.CallbackQuery) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    # Получаем все нужные данные из бд
    user_referrals = await AsyncORM.get_user_referrals(user_id)

    user_referrals_purchased_courses = await AsyncORM.get_referrals_purchased_courses(user_id)

    profile_info = await AsyncORM.get_profile_info(user_id)

    user_balance = profile_info.balance

    user_ref_info = await AsyncORM.get_ref_info(user_id)

    ref_percent = user_ref_info.ref_percent

    if len(user_referrals_purchased_courses) == 0:
        await call.message.answer(profile_text.profile_referrals_dynamics_empty_text.
        format(len(user_referrals), user_balance, ref_percent), reply_markup=profileKeyboards.profile_referrals_back_kb())

        return

    conversionPercent = len(user_referrals_purchased_courses) / len(user_referrals) * 100

    # Получаем курсы, которые были куплены сегодня/в этом месяце/за всё время и потом цену каждого из них присваиваем для константы
    user_referrals_purchased_today_courses: list[PurchasedCoursesOrm] = []
    user_referrals_purchased_thisMonth_courses: list[PurchasedCoursesOrm] = []
    user_referrals_purchased_allTime_courses: list[PurchasedCoursesOrm] = []

    for user_referrals_purchased_course in user_referrals_purchased_courses:
        formatted_purchased_date = datetime.strptime(user_referrals_purchased_course.purchase_date, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()

        if formatted_purchased_date.date() == now.date():
            user_referrals_purchased_today_courses.append(user_referrals_purchased_course)
            user_referrals_purchased_thisMonth_courses.append(user_referrals_purchased_course)

        elif formatted_purchased_date.month == now.month:
            user_referrals_purchased_thisMonth_courses.append(user_referrals_purchased_course)

        user_referrals_purchased_allTime_courses.append(user_referrals_purchased_course)

    user_referrals_purchased_today_courses_totalPrice = user_referrals_purchased_today_courses.reduce(
        lambda acc, purchasedCourse: acc + purchasedCourse.price, 0)

    user_referrals_purchased_thisMonth_courses_totalPrice = user_referrals_purchased_thisMonth_courses.reduce(
        lambda acc, purchasedCourse: acc + purchasedCourse.price, 0)
    
    user_referrals_purchased_allTime_courses_totalPrice = user_referrals_purchased_allTime_courses.reduce(
        lambda acc, purchasedCourse: acc + purchasedCourse.price, 0)

    # Высылаем сообщение
    await call.message.answer(profile_text.profile_referrals_dynamics_text.
    format(conversionPercent, len(user_referrals), len(user_referrals_purchased_courses),
    user_referrals_purchased_today_courses_totalPrice, user_referrals_purchased_thisMonth_courses_totalPrice,
    user_referrals_purchased_allTime_courses_totalPrice, user_balance, ref_percent), reply_markup=profileKeyboards.profile_referrals_back_kb())


async def send_referrals_materials(call: types.CallbackQuery, state: FSMContext) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    await call.message.answer(profile_text.profile_referrals_materials_text,
    reply_markup=profileKeyboards.profile_referrals_back_kb())


def hand_add():
    router.message.register(send_profile_made_payment, StateFilter(ProfileStates.choose_sumOfPayment))

    router.message.register(send_profile_write_cardNumber, StateFilter(ProfileStates.choose_sumOfWithdraw))

    router.message.register(send_profile_confirmation, StateFilter(ProfileStates.write_cardNumber))

    router.callback_query.register(send_profile, lambda c: c.data == 'start|profile')

    router.callback_query.register(send_profile_choose_payment, lambda c: c.data == 'profile|replenish')

    router.callback_query.register(send_profile_choose_sumOfPayment, lambda c: c.data in ["profile_choose_payment|CryptoBot", "profile_choose_payment|bankCard"])

    router.callback_query.register(send_profile_choose_withdraw, lambda c: c.data == 'profile|withdraw')

    router.callback_query.register(send_profile_choose_sumOfWithdraw, lambda c: c.data in ["profile_choose_withdraw|CryptoBot", "profile_choose_withdraw|bankCard"])

    router.callback_query.register(send_withdraw_agree, lambda c: c.data == "profile_confirmation|agree")

    router.callback_query.register(send_referrals_menu, lambda c: c.data == 'profile|referrals')

    router.callback_query.register(send_referrals_dynamics, lambda c: c.data == 'profile_referrals_menu|dynamics')

    router.callback_query.register(send_referrals_materials, lambda c: c.data == 'profile_referrals_menu|materials')