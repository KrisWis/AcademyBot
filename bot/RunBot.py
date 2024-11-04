from aiogram.types import BotCommand
from InstanceBot import bot, dp
import handlers
import asyncio
import logging

async def on_startup() -> None:
    # Определяем команды и добавляем их в бота
    commands = [
        BotCommand(command='/start', description='Перезапустить бота'),
    ]

    await bot.set_my_commands(commands)

    handlers.hand_start.hand_add()

    handlers.profile_hand.hand_add()

    handlers.callhand_start.hand_add()
    
    handlers.webApp_hand.hand_add()
    
    bot_info = await bot.get_me()

    logging.basicConfig(level=logging.INFO)

    print(f'Бот запущен - @{bot_info.username}')

    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(on_startup())
