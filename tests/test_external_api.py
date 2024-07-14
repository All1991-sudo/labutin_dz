import os
from unittest.mock import Mock, patch

from dotenv import load_dotenv

from src.external_api import convert_to_rub

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


def test_convert_to_rub_usd():
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        expected_result = 30000.0
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": expected_result}
        mock_get.return_value = mock_response

        result = convert_to_rub(data, key=API_KEY)
        assert result == expected_result


def test_convert_to_rub_no_key():
    result = convert_to_rub(data, key=None)
    assert result == "Для получения результата конвертации по актуальному курсу введите api ключ."


def test_convert_to_rub_error():
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        result = convert_to_rub(data, key=API_KEY)
        assert result is None


if __name__ == '__main__':
    test_convert_to_rub_usd()
    test_convert_to_rub_no_key()
    test_convert_to_rub_error()
