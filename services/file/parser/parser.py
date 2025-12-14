import io
from abc import ABC, abstractmethod

from services.file.file_manager import FileManager

class BaseFileParser(ABC):
    def __init__(self, file_manager: FileManager, file_id: str, file_name: str):
        self.file_manager = file_manager
        self.file_id = file_id
        self.file_name = file_name

        self.file_data_stream: io.BytesIO | None = None

        # Атрибуты, которые инициализируются только после успешного parser()
        self.file_size: int = 0
        self.language: str | None = None
        self.text: str | None = None

    def get_data(self) -> dict:
        """Возвращает собранные данные в виде словаря для сохранения"""
        return {
            "file_id": self.file_id,
            "file_name": self.file_name,
            "file_size": self.file_size,
            "language": self.language,
            "text": self.text
        }


    @abstractmethod
    async def parse(self):
        """Метод, который реализовывается всеми наследниками"""
        pass