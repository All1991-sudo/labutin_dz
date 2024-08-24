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
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
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
