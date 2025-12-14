from langdetect import detect, LangDetectException
from .parser import BaseFileParser
from cfg.telegram import logger



class MarkdownFile(BaseFileParser):

    """Класс обрабочик марк дауна"""


    async def parse(self):
        self.file_data_stream = await self.file_manager.download_to_buffer(self.file_id)

        if self.file_data_stream is None:
            return f"Не удалось скачать файл: {self.file_id}"

        full_text = []
        combined_text = ""
        try:

            file_size_bytes = len(self.file_data_stream.getvalue())


            markdown_content = self.file_data_stream.read().decode("utf-8")


            local_combined_text = markdown_content.strip()

            detected_lang = "Не определен"

            if local_combined_text:
                try:
                    detected_lang = detect(local_combined_text)
                except LangDetectException:
                    detected_lang = "Не определен (нет текста/ошибка)"

            self.text = local_combined_text
            self.language = detected_lang
            self.file_size = file_size_bytes

            return {f"Data correct added"}

        except Exception as e:
            logger.error(f"Ошибка в парсинге Markdown {self.file_name}", exc_info=True)
            return f"Ошибка при обработке файла {e}"

        finally:
            if self.file_data_stream:
                self.file_data_stream.close()

