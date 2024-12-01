import json
import logging
import re
from typing import Any, Dict, List

import pandas as pd

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def analys_kashback(data: pd.DataFrame, year: int, month: int) -> str:
    """
    Анализирует кэшбэк по категориям за указанный год и месяц.

    Аргументы:
    data (pd.DataFrame): Данные о транзакциях, содержащие столбцы "Дата платежа", "Категория" и "Кэшбэк".
    year (int): Год для анализа (например, 2021).
    month (int): Месяц для анализа (от 1 до 12).

    Возвращает:
    str: JSON-строка, содержащая сумму кэшбэка по категориям за указанный период.
         Если данные некорректны или транзакций нет, возвращает пустой JSON-объект {}.

    Логирование:
    Функция ведет логирование информации о процессе анализа и возможных ошибках.
    """
    try:
        # Проверяем что столбец "Дата платежа" в формате datetime
        if 'Дата платежа' not in data.columns or 'Категория' not in data.columns or 'Кэшбэк' not in data.columns:
            logging.error('В данных отсутствуют необходимые столбцы.')
            return json.dumps({})

        data['Дата платежа'] = pd.to_datetime(data['Дата платежа'], format='%d.%m.%Y', dayfirst=True)

        # Фильтруем данные по году и месяцу
        filtered_transactions = data[
            (data['Дата платежа'].dt.year == year) &
            (data['Дата платежа'].dt.month == month)
            ]

        # Проверка на наличие транзакций
        if filtered_transactions.empty:
            logging.warning(f'Нет транзакций для {year}-{str("0") + str(month)}.')
            return json.dumps({})

        # Суммируем кешбэк по категориям
        cashback_analysis = filtered_transactions.groupby('Категория')['Кэшбэк'].sum()

        cashback_analysis = cashback_analysis[cashback_analysis > 0]

        # Проверка на наличие категорий с положительным кэшбэком
        if cashback_analysis.empty:
            logging.info("Категории с выгодным кэшбэком в указанном месяце отсутствуют!")
            return "Категории с выгодным кэшбэком в указанном месяце отсутствуют!"

        cashback_analysis = cashback_analysis.sort_values(ascending=False)
        cashback_json = json.dumps(cashback_analysis.to_dict(), ensure_ascii=False, indent=4)

        logging.info("Анализ прошёл успешно")
        return cashback_json

    except Exception as e:
        logging.error(f'Ошибка при анализе кешбэка: {e}')
        return json.dumps({})


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Рассчитывает сумму, которую удалось бы отложить в "Инвесткопилку" через округление.

    Аргументы:
    month (str): Месяц в формате 'YYYY-MM'.
    transactions (List[Dict[str, Any]]): Список транзакций с полями 'Дата операции' и 'Сумма операции'.
    limit (int): Порог округления.

    Возвращает:
    float: Сумма, отложенная в «Инвесткопилку».
    """
    pattern_year = r"\b\d{4}\b"
    pattern_month = r"\b\d{2}\b"
    str_year = re.findall(pattern_year, month)
    str_month = re.findall(pattern_month, month)

    # Преобразуем найденные строки в целые числа
    year = int(str_year[0]) if str_year else None
    month_num = int(str_month[0]) if str_month else None

    data = pd.DataFrame(transactions)

    # Преобразуем столбец "Дата операции" в формат datetime
    data["Дата операции"] = pd.to_datetime(data["Дата операции"], format="%d.%m.%Y %H:%M:%S", dayfirst=True)

    # Фильтруем транзакции по году и месяцу
    filtered_transactions = data[
        (data['Дата операции'].dt.year == year) &
        (data['Дата операции'].dt.month == month_num)
        ]

    if filtered_transactions.empty:
        logging.warning(f'Нет транзакций для {year}-{month_num}.')
        return 0.0  # Возвращаем 0.0, если нет транзакций

    positive_transactions = filtered_transactions[filtered_transactions["Сумма операции"] >= 0.0]

    total_saved = 0.0
    for amount in positive_transactions["Сумма операции"]:
        rounded_amount = ((amount // limit) + 1) * limit  # Округление до лимита
        saved_amount = rounded_amount - amount  # Разница между округленным и фактическим
        total_saved += saved_amount

    logging.info(f'Сумма, отложенная в "Инвесткопилку" за {month}: {total_saved:.2f} RUB')
    return total_saved


def search_transactions_by_keyword(transactions: List[Dict[str, Any]], keyword: str) -> str:
    """
    Ищет транзакции по ключевому слову.

    Аргументы:
    transactions (List[Dict[str, Any]]): Список транзакций.
    keyword (str): Ключевое слово для поиска.

    Возвращает:
    str: JSON-ответ со всеми найденными транзакциями.
    """
    results = [transaction for transaction in transactions if
               keyword in str(transaction.get('Категория', '')).lower()]

    if len(results) == 0:
        results = [transaction for transaction in transactions if
                   keyword in str(transaction.get('Описание', '')).lower()]

    logging.info(f'Найдено {len(results)} транзакций по ключевому слову {keyword}.')
    return f"{json.dumps(results, ensure_ascii=False, indent=4)}"


expected_result = [
    {'Дата операции': '01.01.2021', 'Сумма операции': 1000, 'Описание': 'Покупка'}]

print(search_transactions_by_keyword(expected_result, "Покупка"))


def search_transactions_by_phone(transactions: List[Dict[str, Any]]) -> str:
    """
    Ищет транзакции, содержащие мобильные номера в описании.

    Аргументы:
    transactions (List[Dict[str, Any]]): Список транзакций.

    Возвращает:
    str: JSON-ответ со всеми найденными транзакциями.
    """
    phone_pattern = r'\+7\s*\d{3}\s*\d{3}-\d{2}-\d{2}'
    results = [transaction for transaction in transactions if
               re.search(phone_pattern, transaction.get('Описание', ''))]

    logging.info(f'Найдено {len(results)} транзакций с мобильными номерами.')
    return f"{json.dumps(results, ensure_ascii=False, indent=4)}"
