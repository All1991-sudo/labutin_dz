import csv
from typing import Dict, List

import pandas as pd


def read_financial_operations_csv(file_path: str) -> List[Dict[str, str]]:
    """Читает финансовые операции из CSV-файла и возвращает список словарей с транзакциями.

    Args:
        file_path (str): Путь к CSV-файлу.

    Returns:
        List[Dict[str, str]]: Список словарей с транзакциями.
    """
    transactions = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            if "Открытие вклада" in row.get("description", ""):
                deposit = row.get("to")
                if row.get("from") == "":
                    row["from"] = deposit
            for key in row:
                if row[key] == "":
                    row[key] = None
            else:
                transactions.append(row)
    return transactions


def read_financial_operations_excel(file_path: str) -> List[Dict[str, str]]:
    """Читает финансовые операции из Excel-файла и возвращает список словарей с транзакциями.

    Args:
        file_path (str): Путь к Excel-файлу.

    Returns:
        List[Dict[str, str]]: Список словарей с транзакциями.
    """
    df = pd.read_excel(file_path)
    return df.to_dict(orient='records')
