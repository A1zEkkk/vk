from langdetect import detect, LangDetectException
from docx import Document
from .parser import BaseFileParser
from cfg.telegram import logger

class DocxFile(BaseFileParser):

    """Класс обработчик маркдауна"""

    async def parse(self):
        self.file_data_stream = await self.file_manager.download_to_buffer(self.file_id)

        if self.file_data_stream is None:
            return f"Не удалось скачать файл: {self.file_id}"

        full_text = []
        combined_text = ""

        try:
            file_size_bytes = len(self.file_data_stream.getvalue())
            file = Document(self.file_data_stream)

            for paragraph in file.paragraphs:
                full_text.append(paragraph.text)

            combined_text = "\n".join(full_text).strip()

            detected_lang = "Не определен"

            if combined_text:
                try:
                    detected_lang = detect(combined_text)
                except LangDetectException:
                    detected_lang = "Не определен (нет текста/ошибка)"

            self.text = combined_text
            self.language = detected_lang
            self.file_size = file_size_bytes

            return {f"Data correct added"}

        except Exception as e:
            logger.error(f"Ошибка в парсинге PDF {self.file_name}", exc_info=True)
            return f"Ошибка при обработке файла {e}"

        finally:
            if self.file_data_stream:
                self.file_data_stream.close()