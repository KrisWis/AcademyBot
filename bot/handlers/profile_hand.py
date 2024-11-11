from datetime import datetime
from aiogram import types, F
from utils import profile_text
from utils import text
from InstanceBot import router, bot
from database.orm import AsyncORM
from keyboards import profileKeyboards
from states.Student import ProfileStates
from states.Manager import ManagerRefStates
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from credit_card_checker import CreditCardChecker
from database.models import PurchasedCoursesOrm
from utils import cryptoPayment
import asyncio
import os
from utils.const import statuses
import math


# Отправка меню профиля
async def send_profile(call: types.CallbackQuery) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    profile_info = await AsyncORM.get_profile_info(user_id)

    if profile_info.status == statuses["partner"]:
        await call.message.answer(profile_text.partner_profile_text.
        format(profile_info.user.user_reg_date, 
        len(profile_info.completed_courses), ";\n".join(profile_info.completed_courses), profile_info.balance), 
        reply_markup=profileKeyboards.profile_menu())
    else:
        await call.message.answer(profile_text.profile_text.
        format(profile_info.status, profile_info.user.user_reg_date, 
        len(profile_info.completed_courses), ";\n".join(profile_info.completed_courses), profile_info.balance), 
        reply_markup=profileKeyboards.profile_menu())
    

# Отправка меню выбора способа оплаты
async def send_profile_choose_payment(call: types.CallbackQuery, state: FSMContext) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    kb_messageid = await call.message.answer(profile_text.profile_choose_payment_text, 
    reply_markup=profileKeyboards.profile_choose_payment_menu())

    await state.update_data(kb_messageid=kb_messageid.message_id)

    await state.update_data(financeMethod="replenish")


# Отправка меню выбора суммы
async def send_profile_choose_sumOfPayment(call: types.CallbackQuery, state: FSMContext) -> None:
    user_id = call.from_user.id
    methodOfPayment = call.data.split("|")[1]

    data = await state.get_data()

    await bot.delete_message(chat_id=user_id, message_id=data["kb_messageid"])

    await call.message.answer(profile_text.profile_choose_sumOfPayment_text, reply_markup=profileKeyboards.profile_choose_sum_kb())

    await state.update_data(methodOfPayment=methodOfPayment)

    await state.set_state(ProfileStates.choose_sumOfPayment)


# Отправка подтверждения оплаты на пополнение
async def send_profile_made_payment(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    message_id = message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id - 1)

    data = await state.get_data()

    if message.text == "↩️ Назад":
        await message.answer(profile_text.profile_choose_sumOfPayment_text, 
        reply_markup=profileKeyboards.profile_choose_payment_menu())

        return
    
    if len(message.text.split()) > 1:
        payment_summa = int(message.text.split()[0])
    else:
        payment_summa = int(message.text)

    await state.update_data(payment_summa=payment_summa)

    if data["methodOfPayment"] == "CryptoBot": 

        invoice = await cryptoPayment.create_crypto_bot_invoice(payment_summa, "USDT")
        
        await message.answer(profile_text.profile_confirmation_crypto_text.format(payment_summa, invoice.amount),
        reply_markup=profileKeyboards.check_payment_crypto(invoice.bot_invoice_url, invoice.invoice_id))

        await state.set_state(None)

    elif data["methodOfPayment"] == "bankCard":
        await message.answer(profile_text.profile_payment_write_cardNumber_text, reply_markup=types.ReplyKeyboardRemove())

        await state.set_state(ProfileStates.write_cardNumber)


# Обработка подтверждения/отклонения оплаты на пополнение
async def check_crypto_payment(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    username = call.from_user.username
    temp = call.data.split('|')
    data = await state.get_data()
    message_id = call.message.message_id

    if temp[2] == "back":
        await bot.delete_message(chat_id=user_id, message_id=message_id)

        await call.message.answer(profile_text.profile_choose_sumOfPayment_text, reply_markup=profileKeyboards.profile_choose_sum_kb())

        await state.set_state(ProfileStates.choose_sumOfPayment)

        return

    if not await cryptoPayment.check_crypto_bot_invoice(int(temp[2])):
        await call.message.answer(
            text=text.error_payment_text,
            reply_markup=types.ReplyKeyboardRemove(),
            show_alert=True
        )

    else:
        await bot.delete_message(chat_id=user_id, message_id=message_id)
        
        await AsyncORM.change_user_balance(user_id, int(data["payment_summa"]))

        await AsyncORM.add_replenishBalance_info(user_id, int(data["payment_summa"]), datetime.now())

        user_referrer_id = await AsyncORM.get_user_referrer_id(user_id)

        if user_referrer_id:

            user_referrer_percent = await AsyncORM.get_user_ref_percent(user_referrer_id)

            user_referrer_sum = int(int(data["payment_summa"]) * user_referrer_percent / 100)

            await AsyncORM.change_user_balance(user_referrer_id, user_referrer_sum)
            
            await bot.send_message(user_referrer_id, profile_text.successful_referal_replenish_text.format(username, data["payment_summa"], user_referrer_sum))

        await call.message.answer(profile_text.successful_replenish_text.format(data["payment_summa"]), reply_markup=types.ReplyKeyboardRemove())

        await state.set_state(None)

        await state.clear()


# Отправка меню выбора способа вывода
async def send_profile_choose_withdraw(call: types.CallbackQuery, state: FSMContext) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    kb_messageid = await call.message.answer(profile_text.profile_choose_withdraw_text, 
    reply_markup=profileKeyboards.profile_choose_withdraw_menu())

    await state.update_data(kb_messageid=kb_messageid.message_id)

    await state.update_data(financeMethod="withdraw")


# Отправка меню выбора суммы вывода
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


# Отправка сообщения о вводе банковской карте
async def send_profile_write_cardNumber(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    if message.text == "↩️ Назад":
        kb_messageid = await message.answer(profile_text.profile_choose_withdraw_text, 
        reply_markup=profileKeyboards.profile_choose_withdraw_menu())

        await state.update_data(kb_messageid=kb_messageid.message_id)

        await state.set_state(None)

        return

    if len(message.text.split()) > 1:
        sumofWithdraw = int(message.text.split()[0])
    else:
        sumofWithdraw = int(message.text)

    data = await state.get_data()
    
    await state.update_data(sumOfWithdraw=sumofWithdraw)

    if data["methodOfWithdraw"] == "Банковская карта":

        await message.answer(profile_text.profile_withdraw_write_cardNumber_text, reply_markup=types.ReplyKeyboardRemove())

        await state.set_state(ProfileStates.write_cardNumber)

    elif data["methodOfWithdraw"] == "Криптовалюта":
        try:
            check = await cryptoPayment.create_crypto_bot_check(sumofWithdraw)
            
            message_id = await message.answer(profile_text.profile_withDraw_check_text.format(sumofWithdraw), reply_markup=profileKeyboards.send_check_url_kb(check.bot_check_url))
            
            await AsyncORM.change_user_balance(user_id, -sumofWithdraw)

            await AsyncORM.add_withdrawBalance_info(user_id, sumofWithdraw, datetime.now())
            
            while True:
                await asyncio.sleep(30)

                check_info = await cryptoPayment.get_check_info(check.check_id)

                if check_info.status == "activated":
                    break
                    
            await bot.delete_message(chat_id=user_id, message_id=message_id.message_id)

            await message.answer(profile_text.profile_withDraw_check_activated_text, reply_markup=types.ReplyKeyboardRemove())
        except:
            await message.answer(text.error_payment_text, reply_markup=types.ReplyKeyboardRemove())

        await state.set_state(None)

        await state.clear()


# Отправка сообщения с подтверждением данных о выводе
async def send_profile_confirmation(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()

    cart_details = message.text

    if CreditCardChecker(cart_details).valid():

        if data["financeMethod"] == "withdraw":
            await message.answer(profile_text.profile_confirmation_card_text
            .format(cart_details, data["sumOfWithdraw"]), reply_markup=profileKeyboards.profile_confirmation_menu())

            await state.set_state(None)

        if data["financeMethod"] == "replenish":
            await message.answer(profile_text.profile_confirmation_card_text
            .format(cart_details, data["payment_summa"]), reply_markup=profileKeyboards.profile_confirmation_menu())

            await state.set_state(None)
    else: 
        await message.answer(text.invalid_data_text)


# Обработка нажатия на кнопку "✅ Подтвердить" в клавиатуре подтверждения данных
async def click_confirmation_agree(call: types.CallbackQuery, state: FSMContext) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    data = await state.get_data()

    if data["financeMethod"] == "replenish":
        await bot.send_invoice(user_id,
                            title="Пополнение средств",
                            description="Пополнение средств с телеграмм бота на вашу банковскую карту",
                            provider_token=os.getenv("PAYMASTER_API"),
                            currency="rub",
                            prices=[types.LabeledPrice(label="Пополнение средств", 
                                                    amount=int(data["payment_summa"])*100)],
                            start_parameter="replenish-payment",
                            payload="replenish-payload")


# Обработка платежа пользователя на пополнение баланса
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


# Платеж пользователя на пополнение баланса прошёл успешно
async def successful_replenish(message: types.Message, state: FSMContext):

    user_id = message.from_user.id
    username = message.from_user.username

    data = await state.get_data()
    
    await AsyncORM.change_user_balance(message.from_user.id, message.successful_payment.total_amount)
    
    await AsyncORM.add_replenishBalance_info(user_id, message.successful_payment.total_amount, datetime.now())

    user_referrer_id = await AsyncORM.get_user_referrer_id(user_id)

    if user_referrer_id:

        user_referrer_percent = await AsyncORM.get_user_ref_percent(user_referrer_id)

        user_referrer_sum = int(int(data["payment_summa"]) * user_referrer_percent / 100)

        await AsyncORM.change_user_balance(user_referrer_id, user_referrer_sum)
        
        await bot.send_message(user_referrer_id, profile_text.successful_referal_replenish_text.format(username, data["payment_summa"], user_referrer_sum))
        
    await bot.send_message(message.chat.id, profile_text.successful_replenish_text.format(message.successful_payment.total_amount))

    await state.set_state(None)


# Отправка меню "рефералы"
async def send_referals_menu(call: types.CallbackQuery, state: FSMContext) -> None:
    
    user_id = call.from_user.id
    message_id = call.message.message_id
    bot_info = await bot.get_me()
    bot_username = bot_info.username

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    user_status = await AsyncORM.get_user_status(user_id)

    await call.message.answer(profile_text.profile_referals_menu_text.
    format(f'https://t.me/{bot_username}?start={user_id}'), reply_markup=profileKeyboards.profile_referals_menu(user_status))


# Отправка сообщения с динамикой и статистикой рефералов пользователя
async def send_referals_dynamics(call: types.CallbackQuery) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    # Получаем все нужные данные из бд
    user_referals = await AsyncORM.get_user_referals(user_id)

    user_referals_purchased_courses = await AsyncORM.get_referals_purchased_courses(user_id)

    profile_info = await AsyncORM.get_profile_info(user_id)

    user_balance = profile_info.balance

    user_ref_info = await AsyncORM.get_ref_info(user_id)

    ref_percent = user_ref_info.ref_percent

    if len(user_referals_purchased_courses) == 0:
        await call.message.answer(profile_text.profile_referals_dynamics_empty_text.
        format(len(user_referals), user_balance, ref_percent), reply_markup=profileKeyboards.profile_referals_back_kb())

        return

    conversionPercent = len(user_referals_purchased_courses) / len(user_referals) * 100

    # Получаем курсы, которые были куплены сегодня/в этом месяце/за всё время и потом цену каждого из них присваиваем для константы
    user_referals_purchased_today_courses: list[PurchasedCoursesOrm] = await AsyncORM.get_purchased_courses('day')
    user_referals_purchased_thisMonth_courses: list[PurchasedCoursesOrm] = await AsyncORM.get_purchased_courses('month')
    user_referals_purchased_allTime_courses: list[PurchasedCoursesOrm] = await AsyncORM.get_purchased_courses()

    user_referals_purchased_today_courses_totalPrice = user_referals_purchased_today_courses.reduce(
        lambda acc, purchasedCourse: acc + purchasedCourse.price, 0)

    user_referals_purchased_thisMonth_courses_totalPrice = user_referals_purchased_thisMonth_courses.reduce(
        lambda acc, purchasedCourse: acc + purchasedCourse.price, 0)
    
    user_referals_purchased_allTime_courses_totalPrice = user_referals_purchased_allTime_courses.reduce(
        lambda acc, purchasedCourse: acc + purchasedCourse.price, 0)

    # Высылаем сообщение
    await call.message.answer(profile_text.profile_referals_dynamics_text.
    format(conversionPercent, len(user_referals), len(user_referals_purchased_courses),
    user_referals_purchased_today_courses_totalPrice, user_referals_purchased_thisMonth_courses_totalPrice,
    user_referals_purchased_allTime_courses_totalPrice, user_balance, ref_percent), reply_markup=profileKeyboards.profile_referals_back_kb())


# Отправка материалов рефералов пользователя
async def send_referals_materials(call: types.CallbackQuery) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    await call.message.answer(profile_text.profile_referals_materials_text,
    reply_markup=profileKeyboards.profile_referals_back_kb())


# Отправка всех рефералов пользователя
async def send_manager_referals(call: types.CallbackQuery) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    manager_referals = await AsyncORM.get_user_referals(user_id)

    referals_per_page = 10

    pages_amount = math.ceil(len(manager_referals) / referals_per_page)

    if len(manager_referals) > 0:
        await call.message.answer(profile_text.send_manager_referals_text.format(1, pages_amount), 
                                reply_markup=profileKeyboards.manager_referals_kb(manager_referals))
    else:
        await call.message.answer(profile_text.manager_referals_none_text)


# Обработка перелистывания страниц в инлайн клавиатуре рефералов менеджера
async def send_manager_referals_page(call: types.CallbackQuery) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    temp = call.data.split("|")

    page = temp[2]

    action = temp[3]

    if action == "next":
        page = int(page) + 1

    elif action == "prev":
        page = int(page) - 1

    manager_referals = await AsyncORM.get_user_referals(user_id)

    referals_per_page = 10

    pages_amount = math.ceil(len(manager_referals) / referals_per_page)

    await call.message.answer(profile_text.send_manager_referals_text.format(1, pages_amount), 
                        reply_markup=profileKeyboards.manager_referals_kb(manager_referals))


# Отправка данных о реферале менеджера по нажатию на кнопку
async def send_manager_referal_info(call: types.CallbackQuery, state: FSMContext) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    temp = call.data.split("|")

    current_referal_id = int(temp[1])

    await state.update_data(current_referal_id=current_referal_id)

    # Получаем все нужные данные из бд
    current_referal_referals = await AsyncORM.get_user_referals(current_referal_id)

    current_referal_referals_purchased_courses = await AsyncORM.get_referals_purchased_courses(current_referal_id)

    current_referal_profile_info = await AsyncORM.get_profile_info(current_referal_id)

    current_referal_balance = current_referal_profile_info.balance

    current_referal_ref_info = await AsyncORM.get_ref_info(current_referal_id)

    current_referal_ref_percent = current_referal_ref_info.ref_percent

    await call.message.answer(profile_text.send_manager_referal_info_text.format(current_referal_profile_info.user.username))

    if len(current_referal_referals_purchased_courses) == 0:
        await call.message.answer(profile_text.profile_referals_dynamics_empty_text.
        format(len(current_referal_referals), current_referal_balance, current_referal_ref_percent), 
        reply_markup=profileKeyboards.manager_referal_profile_kb())

        return

    conversionPercent = len(current_referal_referals_purchased_courses) / len(current_referal_referals) * 100

    # Получаем курсы, которые были куплены сегодня/в этом месяце/за всё время и потом цену каждого из них присваиваем для константы
    user_referals_purchased_today_courses: list[PurchasedCoursesOrm] = await AsyncORM.get_purchased_courses('day')
    user_referals_purchased_thisMonth_courses: list[PurchasedCoursesOrm] = await AsyncORM.get_purchased_courses('month')
    user_referals_purchased_allTime_courses: list[PurchasedCoursesOrm] = await AsyncORM.get_purchased_courses()

    user_referals_purchased_today_courses_totalPrice = user_referals_purchased_today_courses.reduce(
        lambda acc, purchasedCourse: acc + purchasedCourse.price, 0)

    user_referals_purchased_thisMonth_courses_totalPrice = user_referals_purchased_thisMonth_courses.reduce(
        lambda acc, purchasedCourse: acc + purchasedCourse.price, 0)
    
    user_referals_purchased_allTime_courses_totalPrice = user_referals_purchased_allTime_courses.reduce(
        lambda acc, purchasedCourse: acc + purchasedCourse.price, 0)

    # Высылаем сообщение
    await call.message.answer(profile_text.profile_referals_dynamics_text.
    format(conversionPercent, len(current_referal_referals), len(current_referal_referals_purchased_courses),
    user_referals_purchased_today_courses_totalPrice, user_referals_purchased_thisMonth_courses_totalPrice,
    user_referals_purchased_allTime_courses_totalPrice, current_referal_balance, 
    current_referal_ref_percent), reply_markup=profileKeyboards.manager_referal_profile_kb())
    

# Отправка сообщения для того, чтобы менеджер отправил нужный реферальный процент
async def wait_ref_percent_for_manager_referal(call: types.CallbackQuery, state: FSMContext) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    await call.message.answer(profile_text.write_ref_percent_for_manager_referal_text)

    await state.set_state(ManagerRefStates.write_ref_percent)


# Отправка сообщения об изменении реферального процента реферала менеджера
async def change_ref_percent_for_manager_referal(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    message_id = message.message_id
    username = message.from_user.username

    await bot.delete_message(chat_id=user_id, message_id=message_id - 1)
    
    try:
        future_ref_percent = int(message.text)

        if future_ref_percent < 0 or future_ref_percent > 50:
            await message.answer(profile_text.change_ref_percent_for_manager_referal_error_text)

            return
    except:
        await message.answer(text.invalid_data_text)

    data = await state.get_data()

    current_referal_id = int(data["current_referal_id"])

    previous_ref_percent = await AsyncORM.get_user_ref_percent(current_referal_id)

    current_referal = await AsyncORM.get_user(current_referal_id)

    await AsyncORM.change_user_ref_percent(current_referal_id, future_ref_percent)

    await bot.send_message(current_referal_id, 
                        profile_text.change_ref_percent_manager_referal_text.format(username, previous_ref_percent, future_ref_percent))

    await message.answer(profile_text.change_ref_percent_manager_text.format(current_referal.username, previous_ref_percent, future_ref_percent))

    await state.get_state(None)


def hand_add():
    
    router.message.register(send_profile_made_payment, StateFilter(ProfileStates.choose_sumOfPayment))

    router.message.register(send_profile_write_cardNumber, StateFilter(ProfileStates.choose_sumOfWithdraw))

    router.message.register(send_profile_confirmation, StateFilter(ProfileStates.write_cardNumber))

    router.message.register(change_ref_percent_for_manager_referal, StateFilter(ManagerRefStates.write_ref_percent))

    router.callback_query.register(send_profile, lambda c: c.data == 'start|profile')

    router.callback_query.register(send_profile_choose_payment, lambda c: c.data == 'profile|replenish')

    router.callback_query.register(send_profile_choose_sumOfPayment, lambda c: c.data in ["profile_choose_replenish|CryptoBot", "profile_choose_replenish|bankCard"])

    router.callback_query.register(check_crypto_payment, lambda c: c.data.startswith("payment|CryptoBot"))

    router.callback_query.register(send_profile_choose_withdraw, lambda c: c.data == 'profile|withdraw')

    router.callback_query.register(send_profile_choose_sumOfWithdraw, lambda c: c.data in ["profile_choose_withdraw|CryptoBot", "profile_choose_withdraw|bankCard"])

    router.callback_query.register(click_confirmation_agree, lambda c: c.data == "profile_confirmation|agree")

    router.callback_query.register(send_referals_menu, lambda c: c.data == 'profile|referals')

    router.callback_query.register(send_referals_dynamics, lambda c: c.data == 'profile_referals_menu|dynamics')

    router.callback_query.register(send_referals_materials, lambda c: c.data == 'profile_referals_menu|materials')

    router.callback_query.register(send_manager_referals, lambda c: c.data == 'profile_referals_menu|referals')

    router.callback_query.register(send_manager_referals_page, lambda c: c.data.startswith('manager_referals|page'))

    router.callback_query.register(send_manager_referal_info, lambda c: c.data.startswith('manager_referals'))

    router.callback_query.register(wait_ref_percent_for_manager_referal, lambda c: c.data == "manager_referal|change_percent")

    router.pre_checkout_query.register(pre_checkout_query)

    router.message.register(successful_replenish, F.content_types == types.ContentType.SUCCESSFUL_PAYMENT)