from services.file.file_manager import FileManager
from services.file.parser.pdf import PdfFile
from services.file.parser.txt import TxtFile
from services.file.parser.docx import DocxFile
from services.file.parser.md import MarkdownFile


PARSER_CLASSES = {
    "pdf": PdfFile,
    "txt": TxtFile,
    "docx": DocxFile,
    "md": MarkdownFile,
}

class FileProcessor:
    """Класс координатор, который динамически вызывает нужный класс для обработки"""

    def __init__(self, file_manager: FileManager, file_id: str, file_name: str, file_type: str):
        self.file_manager = file_manager
        self.file_id = file_id
        self.file_name = file_name
        self.file_type = file_type
        self.parser = None # Сюда мы сохраним объект парсера

    async def process_content(self) -> str:
        ParserClass = PARSER_CLASSES.get(self.file_type)
        if not ParserClass:
            return f"Ошибка: Отсутствует класс-обработчик"

        # КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ: сохраняем в self.parser
        self.parser = ParserClass(
            file_manager=self.file_manager,
            file_id=self.file_id,
            file_name=self.file_name
        )

        # Теперь запускаем метод у сохраненного объекта
        result = await self.parser.parse()
        return result

    def get_data(self) -> dict:
        """Метод для получения данных из парсера"""
        if self.parser:
            data = self.parser.get_data()  # вызываем get_data у парсера
            # добавляем file_type, если парсер его не возвращает
            data.setdefault("file_type", self.file_type)
            return data
        return {}


    async def run(self) -> str:
        try:
            return await self.process_content()
        except Exception as e:
            return f"Ошибка: {e}"

