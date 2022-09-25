import asyncio
from bot import commands, listener
from config import settings, dp, logger
from aiogram import executor
import anime_bit


API_TOKEN = settings['API_TOKEN']



async def scheduled(wait_for):
    while True:
        await anime_bit.start()
        await asyncio.sleep(wait_for)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(300))
    executor.start_polling(dp, skip_updates=True, loop=loop)
