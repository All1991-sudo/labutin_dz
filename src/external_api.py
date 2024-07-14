import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('EXCHANGE_RATES_API_KEY')
data = {
    "id": 939719570,
    "state": "EXECUTED",
    "date": "2018-06-30T02:08:58.425572",
    "operationAmount": {
        "amount": "9824.07",
        "currency": {
            "name": "USD",
            "code": "USD"
        }
    }
}


def convert_to_rub(transaction: Dict[str, Any], key: str) -> float | str | Any:
    """
    Конвертация суммы транзакции в рубли. key - необязательный параметр принимающий строку api ключа.
    """
    amount = float(transaction["operationAmount"]['amount'])
    currency = transaction["operationAmount"]['currency']["code"]
    if currency == "RUB":
        return amount
    else:
        if key:
            to_currency = currency
            from_currency = "RUB"

            url = (
                f"https://api.apilayer.com/exchangerates_data/convert"
                f"?to={to_currency}&from={from_currency}&amount={amount}"
            )

            payload = {}
            headers = {
                "apikey": key
            }

            response = requests.get(url, headers=headers, data=payload)

            if response.status_code == 200:
                res = response.json().get("result")
                return float(res)
            else:
                print(f"Error: {response.status_code}")
                return None
        else:
            return "Для получения результата конвертации по актуальному курсу введите api ключ."
