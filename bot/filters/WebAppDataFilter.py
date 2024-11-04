from typing import Union, Dict, Any
from aiogram.filters import Filter
from aiogram.types import Message

class WebAppDataFilter(Filter):
    async def __call__(self, message: Message, **kwargs) -> Union[bool, Dict[str, Any]]:
        return dict(web_app_data=message.web_app_data) if message.web_app_data else False