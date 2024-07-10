import json
import os
from typing import Any, Dict, List


def load_transactions(path: str) -> List[Dict[str, Any]]:
    """ Функция проверяющая по введённому пути файл json. Возвращает пустой список если:
    его нет или содержит ошибку.

        Пример использования:
                            path = 'path/transactions.json'
                            print(load_transactions(path))
    """
    if not os.path.exists(path):
        return []

    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                return []
    except (json.JSONDecodeError, FileNotFoundError):
        return []


# Пример использования функции:
'''file_path = 'path/to/your/transactions.json'
transactions = load_transactions(path)
print(transactions)'''
