from typing import Dict, Generator, Iterable, List

transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {"name": "USD", "code": "USD"},
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {
            "amount": "79114.93",
            "currency": {"name": "USD", "code": "USD"},
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {
            "amount": "43318.34",
            "currency": {"name": "руб.", "code": "RUB"},
        },
        "description": "Перевод со счёта на счёт",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160",
    },
    {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {
            "amount": "56883.54",
            "currency": {"name": "USD", "code": "USD"},
        },
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229",
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount": {
            "amount": "67314.70",
            "currency": {"name": "руб.", "code": "RUB"},
        },
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счет 14211924144426031657",
    },
]


def filter_by_currency(transaction_data: Iterable[Dict], currency: str) -> Generator[Dict, None, None]:
    """
    Функция фильтрует транзакции по валюте.

    Args:
        transaction_data (Iterable[Dict]): Список транзакций для фильтрации.
        currency (str): Код валюты для фильтрации.

    Yields:
        Dict: Транзакция, у которой валюта соответствует заданной валюте.

    """
    if isinstance(transaction_data, (list, tuple)):
        for transaction in transaction_data:
            if (
                    transaction.get("operationAmount", {}).get("currency", {}).get("code")
                    == currency.upper().rstrip()
            ):
                yield transaction


def transaction_descriptions(transact: List[Dict]) -> Generator[str, None, None]:
    """
    Функция извлекает описание транзакций.

    Args:
        transact (List[Dict]): Список транзакций.

    Yields:
        str: Описание каждой транзакции в списке.

    """
    if isinstance(transact, list):
        for transaction in transact:
            try:
                description = transaction["description"]
                yield description
            except KeyError:
                pass


def card_number_generator(start: int, num_card: int) -> Generator[str, None, None]:
    """
    Генерирует номера кредитных карт.

    Args:
        start (int): Начальное значение для генерации номеров.
        num_card (int): Количество карт для сгенерирования.

    Yields:
        str: Сгенерированный номер кредитной карты.

    """
    for i in range(start, num_card):
        card_num = f"{i:016}"
        str_num = " ".join([card_num[x: x + 4] for x in range(0, len(card_num), 4)])
        yield str_num
        start += 1
