from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

# Клавиатура с меню "FAQ"
def faq_menu():
    kb = InlineKeyboardMarkup(
    inline_keyboard=[
    [InlineKeyboardButton(text='1', callback_data='faq|question|1'),
    InlineKeyboardButton(text='2', callback_data='faq|question|2'),
    InlineKeyboardButton(text='3', callback_data='faq|question|3'),
    InlineKeyboardButton(text='4', callback_data='faq|question|4'),
    InlineKeyboardButton(text='5', callback_data='faq|question|5')],
    [InlineKeyboardButton(text='👨‍💻 Задать вопрос', callback_data='faq|support')],
    [InlineKeyboardButton(text='↩️ Назад', callback_data='start_menu')]])

    return kb


# Клавиатура с возвратом в меню "FAQ"
def backTo_faqMenu_kb():
    kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='↩️ Назад', callback_data='start|faq')]])

    return kb