from os import getenv
from dotenv import load_dotenv
from aiogram import Bot
import logging



load_dotenv()
bot = Bot(token=getenv('TOKEN'))
logger = logging.getLogger(__name__)