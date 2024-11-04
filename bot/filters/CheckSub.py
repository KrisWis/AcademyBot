from aiogram.filters import Filter
from aiogram import types
from InstanceBot import bot
from utils import text

# Создаём собственный фильтр на проверку подписки
class Sub(Filter):
    async def __call__(self, message: types.Message) -> bool:
        user_id = message.from_user.id

        user_channel_status = await bot.get_chat_member(chat_id='-1002444021491', user_id=user_id)
        if user_channel_status.status != 'left':
            return True
        else:
            await bot.send_message(message.from_user.id, text.user_not_in_channel_text)

