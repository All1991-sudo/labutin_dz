from src.external_api import convert_to_rub
from unittest.mock import patch


# Тестирование конвертации USD в RUB
def test_conversion_usd_to_rub():
    with patch('src.external_api.get_currency_rate', return_value=75.0):
        transaction = {'amount': 100, 'currency': 'USD'}
        assert convert_to_rub(transaction) == 7500.0


# Тестирование конвертации EUR в RUB
def test_conversion_eur_to_rub():
    with patch('src.external_api.get_currency_rate', return_value=90.0):
        transaction = {'amount': 100, 'currency': 'EUR'}
        assert convert_to_rub(transaction) == 9000.0


# Тестирование конвертации RUB в RUB (должна вернуть исходную сумму)
def test_conversion_rub_to_rub():
    transaction = {'amount': 100, 'currency': 'RUB'}
    assert convert_to_rub(transaction) == 100.0


# Запуск всех тестов
def run_all_tests():
    test_conversion_usd_to_rub()
    test_conversion_eur_to_rub()
    test_conversion_rub_to_rub()


# Запуск тестов
run_all_tests()
