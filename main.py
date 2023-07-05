import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.chat_action import ChatActionMiddleware
#from handlers import router
from config_set import config
from importData import import_report

import time
import schedule


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode='HTML')
    dp = Dispatcher(storage=MemoryStorage())
    # dp.include_router(router=router)
    await bot.delete_webhook(drop_pending_updates=True)
    dp.message.middleware(ChatActionMiddleware())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
