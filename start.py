import asyncio
from aiogram import executor
from telegram import handler
from telegram import keyboard
from service import logger
from telegram.loader import dp
from parsers import anime_bit


async def scheduled(wait_for):
    while True:
        await anime_bit.start()
        await asyncio.sleep(wait_for)


if __name__ == '__main__':
    logger.start()
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(300))
    executor.start_polling(dp, skip_updates=True, loop=loop)
