from InstanceBot import router
from aiogram import types, F
import json
from aiogram.enums.parse_mode import ParseMode

async def parse_data(message: types.Message):
    data = json.loads(message.web_app_data.data)
    await message.answer(f'<b>{data["title"]}</b>\n\n<code>{data["desc"]}</code>\n\n{data["text"]}', parse_mode=ParseMode.HTML)


def hand_add():
    router.message.register(parse_data, F.content_type == types.ContentType.WEB_APP_DATA)