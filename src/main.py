import csv
import json
import re
from collections import Counter
from typing import Dict, List

import pandas as pd


def filter_transactions_by_description(transactions: List[Dict], search_string: str) -> List[Dict]:
    """Фильтрует транзакции по описанию, используя регулярные выражения."""
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)  # Игнорируем регистр
    return [transaction for transaction in transactions if pattern.search(transaction.get('description', ''))]


def count_transactions_by_category(transactions: List[Dict]) -> Dict[str, int]:
    """Подсчитывает количество транзакций по категориям."""
    categories = [transaction['description'] for transaction in transactions]
    return dict(Counter(categories))


# Укажите пути до файлов
file_csv = ""
file_json = ""
file_excel = ""


def load_transactions_from_json(file_path: str):
    """
    Загружает транзакции из JSON-файла.

    Вернёт список транзакций, если файл успешно загружен, иначе пустой список.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: файл '{file_path}' не найден.")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: файл '{file_path}' имеет неверный формат JSON.")
        return []


def load_transactions_from_csv(file_path: str):
    """
    Загружает транзакции из CSV-файла.


    Вернёт список транзакций в виде словарей или если файл не найден, возвращает пустой список.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            return [row for row in reader]
    except FileNotFoundError:
        print(f"Ошибка: файл '{file_path}' не найден.")
        return []


def load_transactions_from_xlsx(file_path: str):
    """
    Загружает транзакции из XLSX-файла.

    Вернёт список транзакций в виде словарей или если файл не найден или произошла ошибка, возвращает пустой список.
    """
    try:
        df = pd.read_excel(file_path)
        return df.to_dict(orient='records')  # Преобразуем DataFrame в список словарей
    except FileNotFoundError:
        print(f"Ошибка: файл '{file_path}' не найден.")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла '{file_path}': {e}")
        return []


def main():
    """
    Основная функция программы, которая предоставляет интерфейс для работы с банковскими транзакциями.
    Позволяет пользователю выбирать источник данных и фильтровать транзакции по статусу и другим критериям.
    """
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Пользователь: ")
    if choice == '1':
        transactions = load_transactions_from_json(file_json)
    elif choice == '2':
        transactions = load_transactions_from_csv(file_csv)
    elif choice == '3':
        transactions = load_transactions_from_xlsx(file_excel)
    else:
        print("Неверный выбор.")
        return

    if transactions:
        status = input(
            "Введите статус, по которому необходимо выполнить фильтрацию "
            "(EXECUTED, CANCELED, PENDING): ").strip().upper()
        valid_statuses = ['EXECUTED', 'CANCELED', 'PENDING']

        while status not in valid_statuses:
            print(f"Статус операции \"{status}\" недоступен.")
            status = input(
                "Введите статус, по которому необходимо выполнить фильтрацию"
                " (EXECUTED, CANCELED, PENDING): ").strip().upper()

        print(f"Операции отфильтрованы по статусу \"{status}\"")
        filtered_transactions = [t for t in transactions if t['state'] == status]

        sort_choice = input("Отсортировать операции по дате? Да/Нет: ").strip().lower()
        if sort_choice == 'да':
            order_choice = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
            filtered_transactions.sort(key=lambda x: x['date'], reverse=(order_choice == 'по убыванию'))

        ruble_choice = input("Выводить только рублевые транзакции? Да/Нет: ").strip().lower()
        if ruble_choice == 'да':
            filtered_transactions = [t for t in filtered_transactions if
                                     t['operationAmount']['currency']['code'] == 'RUB']

        filter_word_choice = input(
            "Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ").strip().lower()
        if filter_word_choice == 'да':
            search_string = input("Введите слово для поиска: ")
            filtered_transactions = filter_transactions_by_description(filtered_transactions, search_string)

        # Подсчет категорий
        category_counts = count_transactions_by_category(filtered_transactions)
        print("Количество транзакций по категориям:")
        for category, count in category_counts.items():
            print(f"{category}: {count}")

        # Вывод результатов
        if not filtered_transactions:
            print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        else:
            print(f"Всего банковских операций в выборке: {len(filtered_transactions)}\n")
            for transaction in filtered_transactions:
                print(f"{transaction['date']} {transaction['description']}")
                print(f"Счет **{transaction['from']}")
                try:
                    print(f"Сумма: {transaction['operationAmount']['amount']}"
                          f" {transaction['operationAmount']['currency']['name']}\n")
                except KeyError:
                    print(
                        f"Сумма: {transaction['amount']} {transaction['currency_name']}\n")
    else:
        print("Программа завершена.")


if __name__ == "__main__":
    main()
