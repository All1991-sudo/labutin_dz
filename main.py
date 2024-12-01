import os
import re
from collections import Counter
from typing import Dict, List

from dotenv import load_dotenv

from src.processing import sorted_dict, sorted_dict_to_time
from src.transaction_read import (read_financial_operations_csv,
                                  read_excel_in_dict)
from src.utils import load_transactions

load_dotenv()
PATH_TO_JSON = os.getenv("PATH_TO_FILE_JS0N")
PATH_TO_CSV = os.getenv("PATH_TO_FILE_CSV")
PATH_TO_XLSX = os.getenv("PATH_TO_FILE_XLSX")


def filter_transactions_by_description(
        transactions: List[Dict], search_string: str
) -> List[Dict]:
    """Фильтрует транзакции по описанию, используя регулярные выражения."""
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)  # Игнорируем регистр
    return [
        transaction
        for transaction in transactions
        if pattern.search(transaction.get("description", ""))
    ]


def count_transactions_by_category(transactions: List[Dict]) -> Dict[str, int]:
    """Подсчитывает количество транзакций по категориям."""
    categories = [transaction["description"] for transaction in transactions]
    return dict(Counter(categories))


def filter_by_currency(transactions: List[Dict], currency_code: str) -> List[Dict]:
    """Фильтрует транзакции по валюте."""
    return [
        t
        for t in transactions
        if t.get("operationAmount", {}).get("currency", {}).get("code") == currency_code
    ]


def main():
    """Основная функция программы."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Пользователь: ")

    if choice == "1":
        print("Для обработки выбран JSON-файл.")
        transactions = load_transactions(PATH_TO_JSON)
    elif choice == "2":
        print("Для обработки выбран CSV-файл.")
        transactions = read_financial_operations_csv(PATH_TO_CSV)
    elif choice == "3":
        print("Для обработки выбран XLSX-файл.")
        transactions = read_excel_in_dict(PATH_TO_XLSX)
    else:
        print("Неверный выбор.")
        return

    if transactions:
        status = (
            input(
                "Введите статус, по которому необходимо выполнить фильтрацию "
                "(EXECUTED, CANCELED, PENDING): "
            )
            .strip()
            .upper()
        )
        valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]

        while status not in valid_statuses:
            print(f'Статус операции "{status}" недоступен.')
            status = (
                input(
                    "Введите статус, по которому необходимо выполнить фильтрацию "
                    "(EXECUTED, CANCELED, PENDING): "
                )
                .strip()
                .upper()
            )

        filtered_transactions = sorted_dict(
            transactions, status
        )  # Фильтрует по статусу

        # Сортировка
        sort_choice = input("Отсортировать операции по дате? Да/Нет: ").strip().lower()
        if sort_choice == "да" or sort_choice == "yes" or sort_choice == "lf":
            order_choice = (
                input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
            )
            ascending = order_choice == "возрастанию"
            filtered_transactions = sorted_dict_to_time(
                filtered_transactions, ascending
            )

        # Фильтрация по валюте
        ruble_choice = (
            input("Выводить только рублевые транзакции? Да/Нет: ").strip().lower()
        )
        if ruble_choice == "да":
            filtered_transactions = filter_by_currency(filtered_transactions, "RUB")

        # Фильтрация по слову в описании
        filter_word_choice = (
            input(
                "Отфильтровать список транзакций по определенному слову в описании? Да/Нет: "
            )
            .strip()
            .lower()
        )
        if filter_word_choice == "да":
            search_string = input("Введите слово для поиска: ")
            filtered_transactions = filter_transactions_by_description(
                filtered_transactions, search_string
            )

        # Подсчет категорий
        category_counts = count_transactions_by_category(filtered_transactions)
        print("Количество транзакций по категориям:")
        for category, count in category_counts.items():
            print(f"{category}: {count}")

        # Вывод результатов
        if not filtered_transactions:
            print(
                "Не найдено ни одной транзакции, подходящей под ваши условия фильтрации."
            )
        else:
            print(
                f"Всего банковских операций в выборке: {len(filtered_transactions)}\n"
            )
            for transaction in filtered_transactions:
                print(
                    f"{transaction.get('date', 'Дата не указана')}\
{transaction.get('description', 'Описание не указано')}"
                )
                print(f"Счет **{transaction.get('from', 'Не указано')}")
                try:
                    print(
                        f"Сумма: {transaction['operationAmount']['amount']}\
{transaction['operationAmount']['currency']['name']}\n"
                    )
                except KeyError:
                    print(
                        f"Сумма: {transaction.get('amount', 'Не указано')}\
{transaction.get('currency_name', 'Не указано')}\n")
    else:
        print("Программа завершена.")


if __name__ == "__main__":
    main()
