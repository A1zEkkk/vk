import asyncio
import logging
import sys

from handlers import dp
from cfg.telegram import bot
from cfg.init import init_nltk

async def main():
    init_nltk()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())