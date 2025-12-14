from aiogram import Router, types, F
from services.file.file_manager import FileManager
from cfg.data import MIME_TYPE_MAP
from cfg.telegram import bot
from services.nltk.datamanager import DataManager
from services.file.file_processor import FileProcessor
import asyncio
from services.table.utils import append_to_google_sheets

file_router = Router()


@file_router.message(F.document)
async def create_data(message: types.Message):
    file_info = message.document
    mime_type = file_info.mime_type

    # Определяем тип файла
    file_type = next((k for k in MIME_TYPE_MAP if MIME_TYPE_MAP[k] in mime_type), None)
    if not file_type:
        return await message.answer(
            "Пожалуйста, выберите другой тип файла (поддерживаются только PDF и TXT)."
        )

    # Создаём менеджер файлов
    file_manager = FileManager(bot=bot)

    # Создаём процессор
    processor = FileProcessor(
        file_manager=file_manager,
        file_id=file_info.file_id,
        file_name=file_info.file_name or "document.pdf",
        file_type=file_type
    )

    # Статус пользователю
    status_msg = await message.answer("⏳ Обрабатываю файл, пожалуйста, подождите...")

    try:
        # Ждём полной обработки файла
        result_text = await processor.run()

        if "Ошибка" in result_text:
            return await message.reply(f"⚠️ Статус: {result_text}")

        # Получаем данные после обработки
        full_results = processor.get_data()
        if not full_results:
            return await message.reply("⚠️ Ошибка: данные файла не получены.")

        # Выводим данные в консоль для проверки
        print("ПОЛУЧЕННЫЕ ДАННЫЕ:")
        for key, value in full_results.items():
            print(f"{key}: {value}")

        await message.reply("✅ Файл обработан. Данные в консоли.")

        # Создаём DataManager и дожидаемся обработки текста
        data_manager = DataManager(processor)
        await data_manager.run()

        await asyncio.to_thread(
            append_to_google_sheets,
            data_manager
        )


    except Exception as e:
        await message.answer(f"Ошибка при обработке файла: {e}")
