from aiogram.types import BotCommand
from InstanceBot import bot, dp
import handlers
import asyncio

async def on_startup() -> None:
    # Определяем команды и добавляем их в бота
    commands = [
        BotCommand(command='/start', description='Перезапустить бота'),
    ]

    await bot.set_my_commands(commands)

    handlers.hand_start.hand_add()
    
    print('Бот запущен')

    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(on_startup())
