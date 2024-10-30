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


def load_transactions_from_json(file_path: str):
    """Загружает транзакции из JSON-файла."""
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
    """Загружает транзакции из CSV-файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            return [row for row in reader]
    except FileNotFoundError:
        print(f"Ошибка: файл '{file_path}' не найден.")
        return []


def load_transactions_from_xlsx(file_path: str):
    """Загружает транзакции из XLSX-файла."""
    try:
        df = pd.read_excel(file_path)
        return df.to_dict(orient='records')  # Преобразуем DataFrame в список словарей
    except FileNotFoundError:
        print(f"Ошибка: файл '{file_path}' не найден.")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла '{file_path}': {e}")
        return []


def filter_by_status(transactions: List[Dict], status: str) -> List[Dict]:
    """Фильтрует транзакции по статусу."""
    return [t for t in transactions if t.get('state') == status]  # Используем get для безопасного доступа к ключу


def sort_transactions(transactions: List[Dict], ascending: bool) -> List[Dict]:
    """Сортирует транзакции по дате."""
    return sorted(transactions, key=lambda x: x.get('date'), reverse=not ascending)


def filter_by_currency(transactions: List[Dict], currency_code: str) -> List[Dict]:
    """Фильтрует транзакции по валюте."""
    return [t for t in transactions if t.get('operationAmount', {}).get('currency', {}).get('code') == currency_code]


def main():
    """Основная функция программы."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    print("Выберите источник данных:")
    print("1. JSON")
    print("2. CSV")
    print("3. XLSX")

    choice = input("Пользователь: ")

    # Запрос пути к файлу в зависимости от выбора
    if choice == '1':
        file_path = input("Введите путь к JSON-файлу: ")
        transactions = load_transactions_from_json(file_path)
    elif choice == '2':
        file_path = input("Введите путь к CSV-файлу: ")
        transactions = load_transactions_from_csv(file_path)
    elif choice == '3':
        file_path = input("Введите путь к XLSX-файлу: ")
        transactions = load_transactions_from_xlsx(file_path)
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
                "Введите статус, по которому необходимо выполнить фильтрацию "
                "(EXECUTED, CANCELED, PENDING): ").strip().upper()

        filtered_transactions = filter_by_status(transactions, status)

        # Сортировка
        sort_choice = input("Отсортировать операции по дате? Да/Нет: ").strip().lower()
        if sort_choice == 'да':
            order_choice = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
            ascending = (order_choice == 'возрастанию')
            filtered_transactions = sort_transactions(filtered_transactions, ascending)

        # Фильтрация по валюте
        ruble_choice = input("Выводить только рублевые транзакции? Да/Нет: ").strip().lower()
        if ruble_choice == 'да':
            filtered_transactions = filter_by_currency(filtered_transactions, 'RUB')

        # Фильтрация по слову в описании
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
                print(
                    f"{transaction.get('date', 'Дата не указана')} {transaction.get('description', 'Описание не указано')}")
                print(f"Счет **{transaction.get('from', 'Не указано')}")
                try:
                    print(
                        f"Сумма: {transaction['operationAmount']['amount']} {transaction['operationAmount']['currency']['name']}\n")
                except KeyError:
                    print(
                        f"Сумма: {transaction.get('amount', 'Не указано')} {transaction.get('currency_name', 
                                                                                            'Не указано')}\n")
    else:
        print("Программа завершена.")


if __name__ == "__main__":
    main()
