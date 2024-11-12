from aiogram import types
from InstanceBot import router, bot
from utils import faq_text
from keyboards import faqKeyboards
from aiogram.fsm.context import FSMContext
from utils import support_text
from states import Student
from helpers import nowIsSupportGraphic

# Отправка меню "FAQ"
async def send_faqMenu(call: types.CallbackQuery, state: FSMContext) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    await call.message.answer(faq_text.faq_menu_text, reply_markup=faqKeyboards.faq_menu())


# Отправка сообщения, чтобы пользователь отправил сообщение в поддержку
async def send_faq_support(call: types.CallbackQuery, state: FSMContext) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    if nowIsSupportGraphic():
        message_text = support_text.support_without_graphic_text
    else:
        message_text = support_text.support_text

    await call.message.answer(message_text, reply_markup=faqKeyboards.backTo_faqMenu_kb())

    await state.set_state(Student.SupportStates.write_text_of_supportTicket)


# Отправка ответа на вопрос по его номеру
async def send_faq_question(call: types.CallbackQuery) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id
    question_number = call.data.split("|")[2]

    await bot.delete_message(chat_id=user_id, message_id=message_id)

    await call.message.answer(faq_text.faq_questions_texts[question_number],
                            reply_markup=faqKeyboards.backTo_faqMenu_kb())


def hand_add():    
    router.callback_query.register(send_faqMenu, lambda c: c.data == 'start|faq')

    router.callback_query.register(send_faq_support, lambda c: c.data == 'faq|support')

    router.callback_query.register(send_faq_question, lambda c: c.data.startswith("faq|question"))