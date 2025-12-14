from gspread import Client, Spreadsheet, Worksheet, service_account
from datetime import datetime, timezone
from typing import List
from services.nltk.datamanager import DataManager


table_link = "https://docs.google.com/spreadsheets/d/1ZBrJnjxnG1ewB4s5PN7D0KXFFHEBaiJ81tHAaJ7J02E/edit?gid=0#gid=0"
table_id = "1ZBrJnjxnG1ewB4s5PN7D0KXFFHEBaiJ81tHAaJ7J02E"

def client_init_json() -> Client:
    """Создание клиента для работы с Google Sheets."""
    return service_account(filename='vkforstazirovka-da0d8a7a0920.json')

def get_table_by_url(client: Client, table_url):
    """Получение таблицы из Google Sheets по ссылке."""
    return client.open_by_url(table_url)


def get_table_by_id(client: Client, table_url):
    """Получение таблицы из Google Sheets по ID таблицы."""
    return client.open_by_key(table_url)

def get_worksheet(client: Client, table_id: str, sheet_index: int = 0) -> Worksheet:
    spreadsheet: Spreadsheet = client.open_by_key(table_id)
    return spreadsheet.get_worksheet(sheet_index)

def append_row_to_table(
    worksheet: Worksheet,
    uploader: str,
    file_name: str,
    summary: str,
    keywords: List[str]
):
    row = [
        datetime.now(timezone.utc).isoformat(),
        uploader,
        file_name,
        summary,
        ", ".join(keywords)
    ]

    worksheet.append_row(row, value_input_option="USER_ENTERED")


def append_to_google_sheets(data_manager: DataManager):
    client = service_account(
        filename="vkforstazirovka-da0d8a7a0920.json"
    )

    table = client.open_by_url(table_link)
    sheet = table.sheet1

    row = [
        datetime.now(timezone.utc).isoformat(),  # timestamp (исправленный вариант)
        "telegram_bot",                          # uploader
        data_manager.file_name,                  # file_name
        data_manager.summary,                    # summary
        ", ".join(data_manager.key_words or [])  # keywords
    ]

    sheet.append_row(row, value_input_option="USER_ENTERED")