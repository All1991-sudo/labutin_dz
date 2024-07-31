import json
import os
from logging_config import setup_logger
from typing import Any, Dict, List


def load_transactions(path: str) -> List[Dict[str, Any]]:
    """Функция проверяющая по введённому пути файл json. Возвращает пустой список если:
    его нет или содержит ошибку.

        Пример использования:
                            path = 'path/transactions.json'
                            print(load_transactions(path))
    """
    logger = setup_logger("utils", "utils.log")
    if not os.path.exists(path):
        logger.info("OK")
        return []
    try:
        logger.info("OK")
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                return []

    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger.error(f"Error: {e}")
        return []
