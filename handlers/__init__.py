from aiogram import Dispatcher
from .file_router.router import file_router

dp = Dispatcher()

dp.include_router(file_router)