import io
from aiogram import Bot
from aiogram.types import File
from cfg.telegram import logger

class FileManager:
    def __init__(self, bot: Bot):
        self.bot = bot

    """Класс для загрузки файла в оперативную память"""


    async def download_to_buffer(self, file_id: str) -> io.BytesIO | None:
        file_buffer = io.BytesIO()

        try:
            logger.info(f"Запись файла id: {file_id} в буффер")

            telegram_file: File = await self.bot.get_file(file_id)
            file_path_on_server = telegram_file.file_path

            if not file_path_on_server:
                logger.error(f"Не удалось получить путь к файлу: {file_id}")
                return None

            await self.bot.download_file(file_path=file_path_on_server, destination=file_buffer)

            file_buffer.seek(0)
            logger.info(f"Скачивание завершено")

            return file_buffer
        except Exception as e:
            logger.error(f"Ошибка при скачивании файла {file_id}: {e}")
            return None