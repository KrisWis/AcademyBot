from aiogram.filters import Filter
from aiogram import types
from InstanceBot import bot
from utils import text
from aiogram.fsm.context import FSMContext

# Создаём собственный фильтр на проверку подписки
class Sub(Filter):
    async def __call__(self, message: types.Message, state: FSMContext) -> bool:
        user_id = message.from_user.id
        referrer_id = message.text[7:] or None

        user_channel_status = await bot.get_chat_member(chat_id='-1002444021491', user_id=user_id)
        if user_channel_status.status != 'left':
            return True
        else:
            await bot.send_message(message.from_user.id, text.user_not_in_channel_text, parse_mode="HTML")
            
            if referrer_id:
                await state.update_data(referrer_id=referrer_id)
