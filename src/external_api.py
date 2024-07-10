import os
import requests
from typing import Dict, Any
API_KEY = os.getenv('EXCHANGE_RATES_API_KEY')


def get_currency_rate(currency_code: str) -> float:
    """Получение текущего курса валюты по отношению к рублю."""
    url = f'https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency_code}&amount=1'
    headers = {'apikey': API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['info']['rate']
    else:
        raise Exception('Ошибка при получении курса валюты')


def convert_to_rub(transaction: Dict[str, Any]) -> float:
    """
    Конвертация суммы транзакции в рубли.
    """
    amount = float(transaction['amount'])
    currency = transaction['currency']

    if currency in ['USD', 'EUR']:
        rate = get_currency_rate(currency)
        return amount * rate
    elif currency == 'RUB':
        return amount
    else:
        raise ValueError('Неизвестный код валюты')
