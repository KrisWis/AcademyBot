from aiogram import Dispatcher, Router, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from Config import TOKEN
from aiogram.client.default import DefaultBotProperties

storage = MemoryStorage()

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()
router = Router()
dp.include_router(router)